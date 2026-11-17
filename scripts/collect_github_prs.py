#!/usr/bin/env python3
import argparse
import datetime
import json
import subprocess
import sys


QUERY = r"""
query($owner:String!,$repo:String!,$limit:Int!) {
  repository(owner:$owner,name:$repo) {
    pullRequests(first:$limit,orderBy:{field:CREATED_AT,direction:DESC}) {
      nodes {
        number title state createdAt updatedAt mergedAt changedFiles additions deletions url
        labels(first:50) { nodes { name } }
        reviews { totalCount }
        closingIssuesReferences(first:20) { nodes { url } }
      }
    }
  }
}
"""


def gh(*args):
    result = subprocess.run(["gh", *args], check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def collect(repository, limit, collected_at):
    owner, repo = repository.split("/", 1)
    metadata = gh("api", f"repos/{repository}")
    license_data = gh("api", f"repos/{repository}/license") if metadata.get("license") else {}
    payload = gh(
        "api", "graphql",
        "-f", f"query={QUERY}",
        "-f", f"owner={owner}",
        "-f", f"repo={repo}",
        "-F", f"limit={limit}",
    )
    pulls = payload["data"]["repository"]["pullRequests"]["nodes"]
    for pull in sorted(pulls, key=lambda item: item["number"]):
        state = "MERGED" if pull["mergedAt"] else pull["state"]
        yield {
            "schema_version": "0.1.0",
            "record_id": f"github:{repository}#pr-{pull['number']}",
            "source": {
                "provider": "github",
                "repository": repository,
                "visibility": metadata["visibility"].upper(),
                "url": pull["url"],
            },
            "pull_request": {
                "number": pull["number"],
                "title": pull["title"],
                "state": state,
                "created_at": pull["createdAt"],
                "updated_at": pull["updatedAt"],
                "merged_at": pull["mergedAt"],
                "changed_files": pull["changedFiles"],
                "additions": pull["additions"],
                "deletions": pull["deletions"],
                "closing_issues": sorted(node["url"] for node in pull["closingIssuesReferences"]["nodes"]),
                "labels": sorted(node["name"] for node in pull["labels"]["nodes"]),
                "review_count": pull["reviews"]["totalCount"],
            },
            "license": {
                "spdx": license_data.get("license", {}).get("spdx_id"),
                "training_eligible": False,
                "review_status": "pending",
            },
            "provenance": {
                "collected_at": collected_at,
                "collector": "scripts/collect_github_prs.py@0.1.0",
                "source_api": "GitHub GraphQL and REST",
            },
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="owner/repository")
    parser.add_argument("--limit", type=int, default=20, choices=range(1, 101), metavar="1..100")
    parser.add_argument("--collected-at", default=datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z"))
    args = parser.parse_args()
    for record in collect(args.repo, args.limit, args.collected_at):
        print(json.dumps(record, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    try:
        main()
    except (subprocess.CalledProcessError, KeyError, ValueError) as error:
        print(f"collection failed: {error}", file=sys.stderr)
        raise SystemExit(1)
