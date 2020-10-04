# Aiven Site Availiability Monitor

This is a simple Python library that uses Aiven Kafka and PostgreSQL services to periodically monitor site availability and send the status to remote DB.

## Configuration
* Place your Kafka access key and certificate files in `keys/` directory (you can download those from Aiven console)
* Setup your monitoring and storage configuration in `conf/config.json`:
```{
    "persistence": {
        "kafka": {
            "uri": "",
            # Ensure this topic is created in your Kafka instance
            "topic": "site-availability"
        },
        # Your Postgres storage configuration
        "postgres": {
            "host": "",
            "port": "",
            "user": "",
            "password": "",
            "dbname": ""
        }
    },
    "monitoring": {
        # The list of sites to monitor
        "http://example.com": {
            "interval": 60, # monitoring frequency (in seconds)
            "regex": null # optional regex pattern to search on page
        },
        "http://google.com": {
            "interval": 180,
            "regex": "html"
        },
        "https://aiven.io": {
            "interval": 30,
            "regex": "no match"
        }
    }
}
```
* Use supplied `schema.sql` to create a monitoring table in your DB

## Usage
Run `docker-compose up` from root directory to get both producer and consumer services up

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
