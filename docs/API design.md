# API Design Document

## Overview
### Websocket Wrapper
All websocket messages, follow a consistent schema.

For requests:
```
{
    "type": <TYPE>,
    "request_id": <CLIENT-GENERATED UID>,
    "payload": {
        <PAYLOAD JSON OBJECT>
    }
}
```

For responses:
```
{
    "type": <TYPE>,
    "request_id": <ECHO OF ASSOCIATED request_id or null>,
    "status": <HTTP status code>,
    "payload": {
        <PAYLOAD JSON OBJECT>
    }
}
```
In responses, the request_id either echos back the id of the request it is responding to, or is `null` if the message is not a response to a specific message (e.g. a message being published as part of a subscription). Types are identical across requests and responses.

## HTTP vs Websocket
Response payloads are identical between many websocket and HTTP responses. Many HTTP requests do not require payloads as the information is encoded in the resource location.

## Subscriptions
Websocket Only. Will get a message when the data for the subscription topic changes
### Subscribing and Unsubscribing
#### Websocket Request
Type: `subscription_begin` or `subscription_end`

Payload:
```
{
    "topic_id": <TOPIC_ID>
}
```
#### Response Payload
```
{
    "timestamp": <SYSTEM UNIX TIMESTAMP>
    "topic_id": <TOPIC_ID>
}
```
### List Subscriptions
To list all current subscriptions on a websocket connection:
#### Websocket Request
Type: `subscription_list`

Payload:
```
{}
``` 
(empty payload)

#### Response Payload
```
{
    "timestamp": <SYSTEM UNIX TIMESTAMP>
    "topics":[
        <LIST OF SUBSCRIBED TOPIC_IDs>
    ]
}
```
## General
### Ping
Returns status and version information.
#### HTTP Request
`GET` `system/ping`
#### Websocket Request
Type: `ping`

Payload:
```
{}
``` 
(empty payload)
#### Response Payload
```
{
    "timestamp": <SYSTEM UNIX TIMESTAMP>,
    "git_hash": <APPLICATION GIT HASH>,
    "git_tag": <APPLICATION GIT TAG>,
}
```
## Experiment Data Download
### Get Archive File
#### HTTP Request
`GET` `/files/archives/<ARCHIVE_ID>`

#### Response Format
**NOTE**: This API call does not return a standard response.

The file will be returned directly, or an error.

### Get Recording File
#### HTTP Request
`GET` `/files/recordings/<RECORDING_ID>`

#### Response Format
**NOTE**: This API call does not return a standard response.

The file will be returned, or an error.

### List Archive Files
#### HTTP Request
`GET` `/files/archives`
#### Websocket Request
Type: `list_files`

Payload:
```
{
    "file_type": "archive"
}
```
#### Response Payload
```
{
    "timestamp": <SYSTEM UNIX TIMESTAMP>,
    "archives": [
        <LIST OF ARCHIVE IDs>
    ]
}
```
### List Recording Files
#### HTTP Request
`GET` `/files/recordings`
#### Websocket Request:
Type: `list_files`

Payload:
```
{
    "file_type": "recording"
}
```
#### Response Payload
```
{
    "timestamp": <SYSTEM UNIX TIMESTAMP>,
    "recordings": [
        <LIST OF RECORD IDs>
    ]
}
```
### Subscription Topics
* `archive_file_list`
* `recording_file_list`
## Application Config
### List Apparatus Config IDs
#### HTTP Request
`GET` `/config/apparatus`
#### Websocket Request:
Type: `list_configs`

Payload:
```
{
    "config_type": "apparatus"
}
```
#### Response Payload
```
{
    "timestamp": <UNIX TIMESTAMP>,
    "configs": [
        <LIST OF APPARATUS_CONFIGS_IDs>
    ]
}
```
### Get Apparatus Config
For a specified apparatus config
#### HTTP Request
`GET` `/config/apparatus/<APPARATUS_CONFIG_ID>`
#### Websocket Request
Type: `get_config`

Payload:
```
{
    "config_type": "apparatus"
    "config_id": <APPARATUS_CONFIG_ID>
}
```
#### Response Payload
```
{
    "timestamp": <UNIX TIMESTAMP>,
    "config_id": <APPARATUS_CONFIG_ID>,
    "content": <FILE CONTENTS>
}
```
### Save Apparatus Config
For a specified apparatus config
#### HTTP Request
`PUT` `/config/apparatus/<APPARATUS_CONFIG_ID>`

Payload: The apparatus config yaml file contents.

#### Websocket Request
Type: `set_config`

Payload:
```
{
    "config_type": "apparatus"
    "config_id": <APPARATUS_CONFIG_ID>
    "content": <FILE CONTENTS>
}
```
#### HTTP Response Payload
The HTTP status code generated
#### Websocket Response Payload
```
{
    "timestamp": <UNIX TIMESTAMP>,
    "config_id": <APPARATUS_CONFIG_ID>,
    "status": <HTTP STATUS CODE>
}
```
### List Alert Config IDs
#### HTTP Request
`GET` `/config/alert`
#### Websocket Request:
Type: `list_configs`

Payload:
```
{
    "config_type": "alert"
}
```
#### Response Payload
```
{
    "timestamp": <UNIX TIMESTAMP>,
    "configs": [
        <LIST OF APPARATUS_CONFIGS_IDs>
    ]
}
```
### Get Alert Config
For a specified alert config
#### HTTP Request
`GET` `/config/alert/<ALERT_CONFIG_ID>`
#### Websocket Request
Type: `get_config`

Payload:
```
{
    "config_type": "alert"
    "config_id": <ALERT_CONFIG_ID>
}
```
#### Response Payload
```
{
    "timestamp": <UNIX TIMESTAMP>,
    "config_id": <ALERT_CONFIG_ID>,
    "content": <FILE CONTENTS>
}
```
### Save Alert Config
For a specified alert config
#### HTTP Request
`PUT` `/config/apparatus/<ALERT_CONFIG_ID>`

Payload: The alert config yaml file contents.

#### Websocket Request
Type: `set_config`

Payload:
```
{
    "config_type": "alert"
    "config_id": <ALERT_CONFIG_ID>
    "content": <FILE CONTENTS>
}
```
#### HTTP Response Payload
The HTTP status code generated
#### Websocket Response Payload
```
{
    "timestamp": <UNIX TIMESTAMP>,
    "config_id": <ALERT_CONFIG_ID>,
    "status": <HTTP STATUS CODE>
}
```
### List Experiment IDs
#### HTTP Request
`GET` `/config/experiment`
#### Websocket Request:
Type: `list_configs`

Payload:
```
{
    "config_type": "experiment"
}
```
#### Response Payload
```
{
    "timestamp": <UNIX TIMESTAMP>,
    "configs": [
        <LIST OF EXPERIMENT_CONFIG_IDs>
    ]
}
```
### Get Experiment Config
For a specified experiment config
#### HTTP Request
`GET` `/config/experiment/<EXPERIMENT_CONFIG_ID>`
#### Websocket Request
Type: `get_config`

Payload:
```
{
    "config_type": "experiment"
    "config_id": <EXPERIMENT_CONFIG_ID>
}
```
#### Response Payload
```
{
    "timestamp": <UNIX TIMESTAMP>,
    "config_id": <EXPERIMENT_CONFIG_ID>,
    "content": <FILE CONTENTS>
}
```
### Save Experiment Config
For a specified experiment config
#### HTTP Request
`PUT` `/config/experiment/<EXPERIMENT_CONFIG_ID>`

Payload: The experiment config yaml file contents.

#### Websocket Request
Type: `set_config`

Payload:
```
{
    "config_type": "experiment"
    "config_id": <EXPERIMENT_CONFIG_ID>
    "content": <FILE CONTENTS>
}
```
#### HTTP Response Payload
The HTTP status code generated
#### Websocket Response Payload
```
{
    "timestamp": <UNIX TIMESTAMP>,
    "config_id": <EXPERIMENT_CONFIG_ID>,
    "status": <HTTP STATUS CODE>
}
```

### Websocket Subscription Topics
* apparatus_config_id_list
* alert_config_id_list
* experiment_id_list

## Experiment Control
### List Loaded Experiment IDs
#### HTTP Request
`GET` `/experiments`
#### Websocket Request:
Type: `list_experiments`

Payload:
```
{}
```
(Empty payload)
#### Response Payload
```
{
    "timestamp": <UNIX TIMESTAMP>,
    "experiments": [
        <LIST OF EXPERIMENT_IDs>
    ]
}
```
### List Experiment Operators
#### HTTP Request
`GET` `/operators`
#### Websocket Request:
Type: `list_operators`

Payload:
```
{}
```
(Empty payload)
#### Response Payload
```
{
    "timestamp": <UNIX TIMESTAMP>,
    "operators": [
        <LIST OF OPERATOR_IDs>
    ]
}
```
### Get Current Experiment ID
#### HTTP Request
`GET` `/active_experiment`
#### Websocket Request:
Type: `get_active_experiment`

Payload:
```
{
    "data": "id"
}
```
#### Response Payload
```
{
    "timestamp": <UNIX TIMESTAMP>,
    "experiment": <ACTIVE EXPERIMENT ID>
}
```

NOTE: The active experiment ID will be `null` if there is no active experiment 
### Get Current Operator IDs
#### HTTP Request
`GET` `/active_experiment/operators`
#### Websocket Request:
Type: `get_active_experiment`

Payload:
```
{
    "data": "operators"
}
```
#### Response Payload
```
{
    "timestamp": <UNIX TIMESTAMP>,
    "operators": [
        <ACTIVE EXPERIMENT OPERATOR IDs>
    ]
}
```

NOTE: The active experiment Operator IDs will be `[null]` if there is no active experiment 

### Start Experiment
#### HTTP Request
`GET` `/active_experiment/<EXPERIMENT_ID>`
#### Websocket Request:
Type: `set_active_experiment`

Payload:
```
{
    "id": <DESIRED EXPERIMENT ID>
}
```
#### HTTP Response Payload
The HTTP status code generated
#### Websocket Response Payload
```
{
    "timestamp": <UNIX TIMESTAMP>,
    "experiment_id": <experiment_ID>,
    "status": <HTTP STATUS CODE>
}
```

### Get Current Segment
#### HTTP Request
`GET` `/active_experiment/segment`
#### Websocket Request:
Type: `get_active_experiment`

Payload:
```
{
    "data": "segment"
}
```
#### Response Payload
```
{
    "timestamp": <UNIX TIMESTAMP>,
    "segment": <ACTIVE EXPERIMENT SEGMENT>
}
```
### Request Halt Experiment
#### HTTP Request
`POST` `/active_experiment/halt`
#### Websocket Request:
Type: `halt_active_experiment`

Payload:
```
{}
```

(Empty payload)
#### HTTP Response Payload
The HTTP status code generated
#### Websocket Response Payload
```
{
    "timestamp": <UNIX TIMESTAMP>,
    "status": <HTTP STATUS CODE>
}
```

### Websocket Subscription Topics
* loaded_experiment_id_list
* current_experiment
* current_segment
* experiment_operators
* segment_ended
* experiment_ended

## Virtual Instruments
### List Virtual Instruments
#### HTTP Request
`GET` `/instrument/`
#### Websocket Request:
Type: `list_instruments`

Payload:
```
{}
```
(Empty payload)
#### Response Payload
```
{
    "timestamp": <UNIX TIMESTAMP>,
    "instruments": [
        <LIST OF VIRTUAL INSTRUMENT IDs>
    ]
}
```
### Get Virtual Instrument Value
#### HTTP Request
`GET` `/instrument/<VIRTUAL INSTRUMENT ID>/value`
#### Websocket Request:
Type: `get_instrument_data`

Payload:
```
{
    "instrument_id": <VIRTUAL INSTRUMENT ID>
    "data": "value"
}
```
#### Response Payload
```
{
    "timestamp": <UNIX TIMESTAMP>,
    "instrument": <VIRTUAL INSTRUMENT ID>
    "value": <VIRTUAL INSTRUMENT VALUE>
}
```
### Set Virtual Instrument Value
#### HTTP Request
`PUT` `/instrument/<VIRTUAL INSTRUMENT ID>/value`

Payload: The value to set the virtual instrument to

#### Websocket Request:
Type: `set_instrument_data`

Payload:
```
{
    "instrument": <VIRTUAL INSTRUMENT ID>
    "data": "value"
    "value": <VALUE>
}
```
#### HTTP Response Payload
The HTTP status code generated
#### Websocket Response Payload
```
{
    "timestamp": <UNIX TIMESTAMP>,
    "instrument": <VIRTUAL INSTRUMENT ID>
    "status": <HTTP STATUS CODE>
}
```
### List Virtual Instrument Recordings
#### HTTP Request
`GET` `/instrument/<VIRTUAL INSTRUMENT ID>/recording`
#### Websocket Request:
Type: `get_instrument_data`

Payload:
```
{
    "instrument": <VIRTUAL INSTRUMENT ID>
    "data": "recordings"
}
```
#### Response Payload
```
{
    "timestamp": <UNIX TIMESTAMP>,
    "instrument": <VIRTUAL INSTRUMENT ID>,
    "recordings": [
        <LIST OF RECORDING IDs>
    ]
}
```
### Get Instrument Recording
#### HTTP Request
`GET` `/instrument/<VIRTUAL INSTRUMENT ID>/recording/<RECORDING_ID>`
#### Websocket Request:
Type: `get_instrument_data`

Payload:
```
{
    "instrument": <VIRTUAL INSTRUMENT ID>
    "data": "record"
    "recording": <RECORDING_ID>
}
```
#### Response Payload
```
{
    "timestamp": <UNIX TIMESTAMP>,
    "instrument": <VIRTUAL INSTRUMENT ID>,
    "recording": <RECORDING_ID>
    "data": <RECORDING DATA>
}
```

### Websocket Subscription Topics
* instrument:<VIRTUAL_INTRUMENT_ID>:value
* instrument:<VIRTUAL_INTRUMENT_ID>:recordings
* instrument:<VIRTUAL_INTRUMENT_ID>:recording:<RECORDING_ID>







