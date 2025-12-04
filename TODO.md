# SNMP Collector Fixes Plan

## Current Issues

1. Database schema mismatch causing "36 values for 37 columns" error
2. SNMP agent names need to be updated:
   - Local collector: "snmp-collector" → "collector-pc"
   - Cloud collector: "snmp-collector" → "collector-cloud"

## Tasks

### 1. Fix Database Schema Issue
- [ ] Identify the exact mismatch between the database schema and INSERT statement
- [ ] Correct the INSERT statement in collector-cloud.py to match the actual database schema
- [ ] Verify that both metrics and last_metrics tables work correctly

### 2. Update SNMP Agent Names
- [x] Updated entrypoint.sh to set sysName based on environment
- [x] Updated collector.py HOSTS definition from "snmp-collector" to "collector-pc"
- [x] Updated collector-cloud.py HOSTS definition from "snmp-collector" to "collector-cloud"
- [ ] Verify that the changes work correctly in both environments

### 3. Update Frontend Filtering Logic
- [x] Modified index.html to use new collector names in filtering
- [ ] Test frontend filtering to ensure it works correctly

### 4. Deploy Changes
- [ ] Deploy fixed collector-cloud.py to cloud server
- [ ] Verify that data collection works without errors
- [ ] Confirm that frontend displays data correctly

## Detailed Analysis

### Database Schema Issue
The error "36 values for 37 columns" indicates that our INSERT statement provides 36 values but the database expects 37 columns. 

Current metrics table schema has 37 columns:
1. id (AUTOINCREMENT)
2. timestamp
3. host
4. cpu
5. memory
6. processes
7. uptime
8. ifOperStatus
9. ifInErrors
10. ifOutErrors
11. ifOperStatus1
12. ifOperStatus2
13. ifOperStatus3
14. ifInErrors1
15. ifInErrors2
16. ifInErrors3
17. ifOutErrors1
18. ifOutErrors2
19. ifOutErrors3
20. linkDown
21. snmpInBadVersions
22. snmpInBadCommunityNames
23. snmpInBadCommunityUses
24. snmpInASNParseErrs
25. snmpInGenErrs
26. snmpInReadOnlys
27. snmpOutTooBigs
28. snmpOutNoSuchNames
29. snmpOutBadValues
30. snmpOutGenErrs
31. snmpInTotalReqVars
32. snmpInTotalSetVars
33. snmpInGetRequests
34. snmpInGetNexts
35. snmpInSetRequests
36. snmpOutGetResponses
37. snmpOutTraps

Our INSERT statement specifies 36 columns (excluding id) but provides 36 values. The error suggests that either:
1. There's a mismatch in our column list vs actual database
2. There's an issue with how we're counting the placeholders

Need to carefully check:
- Column names in INSERT statement match database exactly
- Number of placeholders (?) matches number of columns
- Number of values in tuple matches number of placeholders

## Next Steps

1. Double-check the column list in INSERT statement against database schema
2. Count placeholders in VALUES clause
3. Count values in the tuple
4. Ensure all three numbers match