import ezylogs

ezylogs.setup({
    "apiKey": "my-api-key",
    "system": "another-system"
})

ezylogs.debug({"test": "test1 arg1dsdsd"})
ezylogs.monitor()