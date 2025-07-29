# Brivo Smarthome Python Client

A Python client library for communicating with Brivo Smarthome, providing an easy interface for managing authentication and
interacting with Brivo's API.

## Installation

```sh
pip install brivo
```

## Example Usage

```python
import brivo

# Initialize the client
brivo = brivo.BrivoClient(username='your_user_name', password='your_password')

# Get users
users = brivo.users()
print(users)

# Create a new unit
new_unit = brivo.create_unit(...)
print(new_unit)
```

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License.
