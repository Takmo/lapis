# API Documentation

This document serves as a planning area for an API related to this service.

All API calls are submitted over HTTPS and must include `username` and
`password` fields that successfully authenticate a user. A response will
always be returned as parseable JSON containing at least a `returncode`
integer value and a `response` string containing corresponding information.

returncode | response
-----------|---------
0 | success
1 | command failure
2 | authentication failure
3 | internal server error
-1 | API unavailable

Should the API be unavailable, the returncode and response will indicate as such
and no further information will be provided.

In the event of a command failure, `failurecode` and `failuredesc` fields will
be filled in with an integer value and string description respectively.

If the `username` and `password` fields fail authentication, the returncode and
response will reflect this and no further information will be provided.

In the event that there is a malfunction on the server side, the returncode and
response will indicate this. Further information on the error may be provided
depending on server side configuration or user authentication. Note that in this
situation, an internal server errors does not always mean a complete command
failure, and further action may be required.

More information on API calls, as well as any additional information they may
return, can be found below.

### /server/start

Attempts to start the server. This command will fail if the server is not in the
`stopped` phase. A successful return denotes that the server has transitioned
from the `stopped` phase to the `starting` phase.

### /server/status

Returns one of four states that the server is currently in.

* `stopped` - the server is inactive.
* `starting` - the server is being provisioned and setup.
* `running` - the server is currently active and should be accessible.
* `stopping` - the state is being saved and the server is being terminated.

### /server/stop

Attempts to stop the server. This command will fail if the server is already in
the `stopped` or `stopping` phase. A successful return denotes that the server
has transitioned from `running` to `stopping`, or if the server is currently
`starting`, that it will transition from `running` to `stopping` once `starting`
is complete.

