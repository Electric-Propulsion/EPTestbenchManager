# API Design Document

## Generic API Call Structure
### HTTP

### Websockets

## General
### ping
Returns status and version information
#### HTTP
#### Websocket

### Subscriptions
Websocket Only. Will get a message when the data for the subscription topic changes
#### Subscribing and Unsubscribing:
To subscribe to a topic:
```
{
    "type": "subscription_begin",
    "topic_id": <TOPIC_ID>
}
```
To unsubscribe to a topic:
```
{
    "type": "subscription_end",
    "topic_id": <TOPIC_ID>
}
```
Success or failure response to either of the above:
```
{
    "type": <subscription_begin" OR "subscription_end">
    "timestamp": <SYSTEM UNIX TIMESTAMP>
    "topic_id": <TOPIC_ID>
    "status": <"ok" OR "fail">
    "info": <INFORMATIONAL TEXT>
}
```
#### To List subscriptions
To list all current subscriptions on a websocket connection:
```
{
    "type": "subscription_list"
}
```
Typical response:
```
{
    "type":" "subscription_list"
    "timestamp": <SYSTEM UNIX TIMESTAMP>
    "topics":[
        <LIST OF SUBSCRIBED TOPIC_IDs>
    ]
}
```

## Experiment Data Download
### get_archive_file
#### HTTP
### get_experiment_file
#### HTTP
### list_archive_files
#### HTTP
#### Websocket
### list_recording_files
#### HTTP
#### Websocket
### Websocket Subscription Topics
* archive_file_list
* recording_file_list

## Application Config
### list_apparatus_config_ids
#### HTTP
#### Websocket
### get_apparatus_config
For a specified apparatus config
#### HTTP
#### Websocket
### save_apparatus_config
For a specified apparatus config
#### HTTP
#### Websocket
### list_alert_config_ids
#### HTTP
#### Websocket
### get_alert_config
For a specified alert config
#### HTTP
#### Websocket
### save_alert_config
For a specified alert config
#### HTTP
#### Websocket
### list_experiment_ids
#### HTTP
#### Websocket
### get_experiment_config
For a specified experiment config
#### HTTP
#### Websocket
### Websocket Subscription Topics
* apparatus_config_id_list
* alert_config_id_list
* experiment_id_list

## Experiment Control
### list_loaded_experiment_ids
#### HTTP
#### Websocket
### list_experiment_operators
#### HTTP
#### Websocket
### get_current_experiment
#### HTTP
#### Websocket
### start_experiment
#### HTTP
#### Websocket
### get_current_segment
#### HTTP
#### Websocket
### request_halt_experiment
#### HTTP
#### Websocket

### Websocket Subscription Topics
* loaded_experiment_id_list
* current_experiment

    Note: show what the data segment for these would be, and for others

* current_segment
* experiment_operators
* segment_ended
* experiment_ended

## Virtual Instruments
### list_virtual_instruments
#### HTTP
#### Websocket
### get_value
#### HTTP
#### Websocket
### set_value
#### HTTP
#### Websocket
### list_instrument_recordings
#### HTTP
#### Websocket
### get_instrument_recording
#### HTTP
#### Websocket

### Websocket Subscription Topics
* instrument:<VIRTUAL_INTRUMENT_ID>:value
* instrument:<VIRTUAL_INTRUMENT_ID>:recordings
* instrument:<VIRTUAL_INTRUMENT_ID>:recording:<RECORDING_ID>







