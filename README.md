# Bot for tracking, approving, and denying belt requests for LPU discord.

## Requirements

Requires python > `3.8`
`pip install discord`

Bot setup:

Requires priviledged intent `members`.

Requires; [
    "Manage Roles",
    "Send Messages",
    "Read Message History"
]

Requires env var `BELTBOT_TOKEN`.
Requires access to a json file. You can configure this however you please in the `DATA_FILE` constant.


## Command reference:

#### Making a belt request
`.beltrequest <colour> <anychar> <request text>`
Example: `.beltrequest white - Hi I picked a 410 with a toothbrush

Example output:
```
@ theelous3 thanks for your White Belt request!
```

#### Listing active requests

`.beltlist [order]`

For order, you can pass `oldest` or `newest`.

Example output:
```
Active requests, sorted by oldest:

Created: 2021-02-14 23:04:12
ID: 9f542352g718
User: `@theelous3`
Belt: white
Message: Hi I picked a 410 with a toothbrush
URL: https://discord.com/channels/345y7289523/6226464564456/6245645224566542564

Created: 2021-02-14 22:02:16
ID: af545352g712
User: `@theelous3`
Belt: yellow
Message: Abus 65/60 https://youtube.com/watch?423horuiwbfnwoi
URL: https://discord.com/channels/345y7289523/6226464564456/g345h789gbniuerlgb4
```

### Role protected commands

#### Approving a request

As you can see, requests have IDs. You can use this ID to interact with it.

`.beltapprove <request_id> [note text]`

Example:
`.beltapprove 9f542352g718 Nice pick!`

This will ping the applicant and assign them the requested role, like so:

```
@theelous3, @moderatorGuy has reviewed and approved your request. Congrats on your White Belt!
Notes: Nice pick!
```

#### Rejecting a request

`.beltreject <request_id> <reason text>`

You must provide a reason when denying a request.

Example: `.beltreject af545352g712 That isn't a lock, it's a beer can`

This will ping the applicant and reject the application, like so:

```
@theelous3, @moderatorGuy has reviewed and denied your request for White Belt.
Notes: That isn't a lock, it's a beer can
```


#### Requesting more info

`.beltmoreinfo <request_id> <reason text>`

You must provide a reason when requesing more info.

Example: `.beltmoreinfo af545352g712 you need to gut the lock in the same take, sorry`

```
@theelous3, @moderatorGuy has reviewed your request for White Belt but needs more information. Please update your request here: https://discord.com/channels/345y7289523/6226464564456/g345h789gbniuerlgb4
Notes: you need to gut the lock in the same take, sorry
```
