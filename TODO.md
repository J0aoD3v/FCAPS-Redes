# TODO: Modify Dashboard to Show Only Local Hosts with Uptime 0

## Tasks

- [ ] Edit index.html loadData() function to filter hosts
  - Filter to only local hosts (exclude oracle-cloud, api-daora, instance-20251116-2130)
  - Filter to only hosts with uptime === 0
  - This should leave alpine-host, nginx-web, python-app
- [ ] Update stats calculation to use filtered hosts
- [ ] Update charts to use filtered hosts
- [ ] Update host cards rendering to use filtered hosts
- [ ] Test the changes by running the dashboard
