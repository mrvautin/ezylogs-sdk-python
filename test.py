import ezylogs

ezylogs.setup({
    "apiKey": "my-api-key",
    "system": "my-system-name"
})

ezylogs.debug({"Variable": "My variable value"})
ezylogs.error({"Error": "System crashed"})
ezylogs.monitor()