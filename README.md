# ansible-playbook action - simple Ansible playbooks for GitHub Actions

`ansible-action` speeds up and simplifies using `ansible-playbook` inside your
GitHub Action workflows by downloading a pre-built docker image for speedy
builds. This has the benefit of being faster that manually installing
`ansible` and its dependencies on every workflow run.

## Usage

Using this workflow is as simple as:

```yaml
jobs:
  some_job:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: amplium/ansible-action@master
        with:
          playbook: path/to/playbook.yaml
          inventory: path/to/inventory.yaml
          requirements: |
            path/to/requirements.yaml
            other/path/to/requirements.yaml
          extra_vars: |
            some_var=some_value
            some_secret=${{ secrets.SOME_SECRET }}
```

## Inputs

- inventory (required): Name of the inventory file in your workspace.
- playbook (required): Name of the playbook in your workspace.
- requirements (optional): Name of the galaxy file in your workspace.
- limit (optional): Further limit selected hosts to an additional pattern.
- skip_tags (optional): Only run plays and tasks whose tags do not match these values.
- start_at_task (optional): Start the playbook at the task matching this name.
- tags (optional): Only run plays and tasks tagged with these values.
- extra_vars (optional): Set additional variables as key=value.
- module_path (optional): Prepend paths to module library.
- check (optional): Run a check, do not apply any changes.
- diff (optional): When changing (small) files and templates, show the differences in those files; works great with –check.
- flush_cache (optional): Clear the fact cache for every host in inventory.
- force_handlers (optional): Run handlers even if a task fails.
- list_hosts (optional): Outputs a list of matching hosts.
- list_tags (optional): List all available tags.
- list_tasks (optional): List all tasks that would be executed.
- syntax_check (optional): Perform a syntax check on the playbook.
- forks (optional): Specify number of parallel processes to use.
- vault_id (optional): The vault identity to use.
- vault_password (optional): The vault password to use.
- verbose (optional): Level of verbosity, 0 up to 4.
- private_key (optional): Use this key to authenticate the connection.
- user (optional): Connect as this user.
- connection (optional): Connection type to use.
- timeout (optional): Override the connection timeout in seconds.
- ssh_common_args (optional): Specify common arguments to pass to ssh/scp/sftp.
- ssh_extra_args (optional): Specify extra arguments to pass to ssh only.
- scp_extra_args (optional): Specify extra arguments to pass to scp only.
- sftp_extra_args (optional): Specify extra arguments to pass to sftp only.
- become (optional): Run operations with become.
- become_method (optional): Privilege escalation method to use.
- become_user (optional): Run operations as this user.
- options (optional): Additional options to pass to the ansible-playbook CLI.

## License

This GitHub Action is licensed under the [MIT License](./LICENSE)
