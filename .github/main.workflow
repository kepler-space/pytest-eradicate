workflow "Test" {
  on = "push"
  resolves = ["test"]
}

action "test" {
  uses = "docker://python:3.6"
  runs = ["/bin/sh", "-c", "set -xe; pip install -e .; ! py.test --eradicate setup.py; py.test --eradicate ./pytest_eradicate.py"]
}