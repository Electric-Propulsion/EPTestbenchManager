# API Design Document

## Generic API Call Structure
### HTTP

### Websockets

## General
### ping
Returns status and version information
#### HTTP
#### Websocket

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

## Application Config
### list_apparatus_configs
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
### list_alert_configs
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
### list_experiment_config
#### HTTP
#### Websocket
### get_experiment_config
For a specified experiment config
#### HTTP
#### Websocket

## Experiment Control
### list_loaded_experiment_IDs
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

### Websocket Subscriptions
* current_experiment
* current_segment
* experiment_operators
* segment_ended
* experiment_ended








