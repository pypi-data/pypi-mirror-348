# SWIFT Parser (Python)

A Python parser for [ISO 15022](http://www.iso15022.org/) messages used for messaging in securities trading by the [SWIFT network](http://www.swift.com/). This parser is designed to handle the standard format of SWIFT financial messages.

[![PyPI version](https://badge.fury.io/py/swift-parser-py.svg)](https://badge.fury.io/py/swift-parser-py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

* Parses any FIN MT message defined by the [ISO 15022](http://www.iso15022.org/) standard
* Supports Block 1, Block 2, Block 3 (User Header), Block 4 (Message Content), and Block 5 (Trailer)
* Extensive field pattern support with over 100 different field formats
* Parses structured fields (including complex fields like 50K, 59, etc.)
* Non-validating - generously parses messages not 100% compliant with the ISO standard
* One-way parsing only - doesn't generate MT messages
* Metadata-driven approach using field pattern definitions
* Handles complex nested blocks and multi-line fields
* Produces a structured Abstract Syntax Tree (AST) representation of messages
* Robust error handling for malformed fields

## Installation

### From PyPI

```Shell
$ pip install swift-parser-py
```

### From Source

```Shell
$ git clone https://github.com/solchos/swift-parser.git
$ cd swift-parser
$ pip install -e .
```

## Usage

```python
from swift_parser_py.swift_parser import SwiftParser

# Initialize the parser
parser = SwiftParser()

# Parse a SWIFT message
with open('message.txt', 'r') as file:
    swift_message = file.read()

# Method 1: Using process() for direct result
result = parser.process(swift_message)
print(result)

# Method 2: Using parse() with a callback
def callback(err, result):
    if err:
        print(f"Error: {err}")
    else:
        print(result)

parser.parse(swift_message, callback)
```

It is also possible to run the parser from the command line:

```Shell
$ python -m swift_parser_py.swift_parser path/to/message.txt
```

## Architecture

The parser is composed of several specialized components:

### Core Components

* **SwiftParser**: Main entry point that orchestrates the parsing process
* **FinParser**: Parses the high-level block structure of SWIFT messages
* **MtParser**: Parses the fields within Block 4 (Message Text)
* **Block-specific parsers**:
  * `block1_parser.py`: Parses Block 1 (Basic Header)
  * `block2_parser.py`: Parses Block 2 (Application Header)
  * `block3_parser.py`: Parses Block 3 (User Header, optional)
  * `block5_parser.py`: Parses Block 5 (Trailer, optional)

### Field Parsing

* **FieldParser**: Parses individual field content based on field patterns
* **FieldRegexpFactory**: Generates regular expressions for field validation
* **Field pattern definitions**: Stored in `metadata/patterns.json`

### Block 5 (Trailer) Support

The parser fully supports Block 5 (Trailer) with the following features:

* Parses all standard Block 5 tags:
  * `CHK`: Checksum (mandatory)
  * `TNG`: Test & Training Message (optional)
  * `PDE`: Possible Duplicate Emission (optional)
  * `DLM`: Delayed Message (optional)
  * `MRF`: Message Reference (optional)
  * `PDM`: Possible Duplicate Message (optional)
  * `SYS`: System Originated Message (optional)
* Provides detailed parsing for structured tags:
  * Extracts time, date, BIC, session number, and sequence number from PDE, PDM, and SYS tags
  * Extracts date, time, original date, BIC, session number, and sequence number from MRF tags
* Handles empty tag values correctly
* Maintains the original content structure for reference

### Parsing Process

1. The message is first parsed into blocks using `FinParser`
2. Each block is then parsed by its specific parser
3. For Block 4, fields are extracted using `MtParser`
4. Each field's content is parsed using pattern definitions
5. For Block 5, tags are extracted and structured data is parsed
6. The result is a structured AST (Abstract Syntax Tree)

## Field Patterns Support

The parser supports an extensive set of field patterns as defined in the ISO 15022 standard:

* Basic field types (16x, 35x, etc.)
* Currency and amount fields (3!a15d)
* Date and time fields (6!n, 8!n, etc.)
* Complex structured fields (addresses, multi-line fields)
* Special field formats for different message types

For more details about field patterns, see [FIELD_PATTERNS.md](swift_parser_py/docs/FIELD_PATTERNS.md)

## Message Types Support

The parser supports all standard SWIFT MT message types, including but not limited to:

* MT101: Request for Transfer
* MT103: Single Customer Credit Transfer
* MT202: General Financial Institution Transfer
* MT202COV: Cover Payment
* MT205: Financial Institution Transfer Execution
* MT900: Confirmation of Debit
* MT910: Confirmation of Credit
* MT940: Customer Statement
* MT942: Interim Statement
* MT950: Statement Message

## Example

Parsing this SWIFT message:

```
{1:F01EXAMPLEBANK0001000001}{2:I103RECEIVERBANK0000N}{3:{108:MSGREF2023}{121:REF-XYZ-789}}{4:
:20:CUSTREF2023-001
:23B:CRED
:32A:230803USD5000,00
:33B:USD5000,00
:50K:/87654321
SENDER COMPANY LTD
123 SENDER STREET, CITY
:52A:ORDERBANK
:53A:SENDERBANK
:57A:RECEIVERBANK
:59:/12345678
BENEFICIARY NAME
15 BENEFICIARY ROAD
:70:PAYMENT FOR SERVICES
INVOICE 2023-001
:71A:SHA
:72:/ACC/INTERNAL TRANSFER
-}{5:{CHK:123456789ABC}{PDE:1348120811BANKFRPPAXXX2222123456}}
```

Results in a structured dictionary with blocks and parsed fields:

```json
{
  "block1": {
    "block_id": 1,
    "content": "F01EXAMPLEBANK0001000001",
    "application_id": "F",
    "service_id": "01",
    "receiving_lt_id": "EXAMPLEBANK0",
    "session_number": "0010",
    "sequence_number": "00001"
  },
  "block2": {
    "content": "I103RECEIVERBANK0000N",
    "block_id": 2,
    "direction": "I",
    "msg_type": "103",
    "bic": "RECEIVERBA",
    "prio": "N"
  },
  "block3": {
    "block_id": 3,
    "tags": {
      "108": "MSGREF2023",
      "121": "REF-XYZ-789"
    },
    "content": [
      {
        "name": "108",
        "content": [
          "MSGREF2023"
        ]
      },
      {
        "name": "121",
        "content": [
          "REF-XYZ-789"
        ]
      }
    ]
  },
  "block4": {
    "fields": [
      {
        "type": "20",
        "option": "",
        "fieldValue": "CUSTREF2023-001",
        "content": ":20:CUSTREF2023-001",
        "ast": {
          "Reference Number": "CUSTREF2023-001"
        }
      },
      {
        "type": "23",
        "option": "B",
        "fieldValue": "CRED",
        "content": ":23B:CRED",
        "ast": {
          "Bank Operation Code": "CRED"
        }
      },
      {
        "type": "32",
        "option": "A",
        "fieldValue": "230803USD5000,00",
        "content": ":32A:230803USD5000,00",
        "ast": {
          "Date": "230803",
          "Currency": "USD",
          "Amount": "5000,00"
        }
      },
      {
        "type": "33",
        "option": "B",
        "fieldValue": "USD5000,00",
        "content": ":33B:USD5000,00",
        "ast": {
          "Currency": "USD",
          "Instructed Amount": "5000,00"
        }
      },
      {
        "type": "50",
        "option": "K",
        "fieldValue": "/87654321\nSENDER COMPANY LTD\n123 SENDER STREET, CITY",
        "content": ":50K:/87654321\nSENDER COMPANY LTD\n123 SENDER STREET, CITY",
        "ast": {
          "Account": "/87654321",
          "Name": "SENDER COMPANY LTD",
          "Address": ["123 SENDER STREET, CITY"],
          "Name and Address": ["SENDER COMPANY LTD", "123 SENDER STREET, CITY"]
        }
      },
      {
        "type": "52",
        "option": "A",
        "fieldValue": "ORDERBANK",
        "content": ":52A:ORDERBANK",
        "ast": {
          "BIC": "ORDERBANK"
        }
      },
      {
        "type": "53",
        "option": "A",
        "fieldValue": "SENDERBANK",
        "content": ":53A:SENDERBANK",
        "ast": {
          "BIC": "SENDERBANK"
        }
      },
      {
        "type": "57",
        "option": "A",
        "fieldValue": "RECEIVERBANK",
        "content": ":57A:RECEIVERBANK",
        "ast": {
          "BIC": "RECEIVERBANK"
        }
      }
      // Additional fields omitted for brevity
    ]
  },
  "block5": {
    "block_id": 5,
    "tags": {
      "CHK": "123456789ABC",
      "PDE": "1348120811BANKFRPPAXXX2222123456"
    },
    "content": [
      {
        "name": "CHK",
        "content": [
          "123456789ABC"
        ]
      },
      {
        "name": "PDE",
        "content": [
          "1348120811BANKFRPPAXXX2222123456"
        ]
      }
    ],
    "pde_details": {
      "time": "1348",
      "date": "120811",
      "bic": "BANKFRPPAXXX",
      "session_number": "2222",
      "sequence_number": "123456"
    }
  }
}

## Usage Examples

### 1. Basic Parsing

```python
from swift_parser_py.swift_parser import SwiftParser

# Initialize the parser
parser = SwiftParser()

# Parse a SWIFT message
swift_message = "{1:F01EXAMPLEBANK0001000001}{2:I103RECEIVERBANK0000N}..."
result = parser.process(swift_message)

# Access basic message information
msg_type = result['block2']['msg_type']  # "103"
sender_bic = result['block2']['bic']     # "RECEIVERBA"

# Access specific fields
reference = result['block4']['fields'][0]['fieldValue']  # "CUSTREF2023-001"
amount = result['block4']['fields'][2]['ast']['Amount']  # "5000,00"
currency = result['block4']['fields'][2]['ast']['Currency']  # "USD"
sender_name = result['block4']['fields'][4]['ast']['Name']  # "SENDER COMPANY LTD"
beneficiary_account = result['block4']['fields'][8]['ast']['Account']  # "/12345678"
```

### 2. Callback-Based Processing

```python
from swift_parser_py.swift_parser import SwiftParser

def message_callback(err, result):
    if err:
        print(f"Error parsing message: {err}")
    else:
        # Process the result
        print(f"Message type: MT{result['block2']['msg_type']}")
        print(f"Reference: {result['block4']['fields'][0]['fieldValue']}")
        print(f"Amount: {result['block4']['fields'][2]['ast']['Amount']} {result['block4']['fields'][2]['ast']['Currency']}")

# Initialize the parser
parser = SwiftParser()

# Parse with callback
parser.parse(swift_message, message_callback)
```

### 3. Command-Line Usage

You can run the parser directly from the command line:

```bash
# Using the module
python -m swift_parser_py.swift_parser path/to/message.txt

# Output will be printed to the console in JSON format
```

### 4. Processing Multiple Messages

```python
import os
from swift_parser_py.swift_parser import SwiftParser

def process_directory(directory_path):
    parser = SwiftParser()
    results = []

    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as file:
                swift_message = file.read()
                try:
                    result = parser.process(swift_message)
                    results.append({
                        'filename': filename,
                        'parsed': result,
                        'status': 'success'
                    })
                except Exception as e:
                    results.append({
                        'filename': filename,
                        'error': str(e),
                        'status': 'error'
                    })

    return results

# Process all messages in a directory
results = process_directory('path/to/messages')
```

### 5. Error Handling

```python
from swift_parser_py.swift_parser import SwiftParser

parser = SwiftParser()

# Method 1: Using try/except
try:
    result = parser.process(swift_message)

    # Check for field parsing errors
    for field in result['block4']['fields']:
        if 'ast' in field and 'error' in field['ast']:
            print(f"Warning: Field {field['type']}{field.get('option', '')} parsing error: {field['ast']['error']}")

except Exception as e:
    print(f"Error parsing message: {e}")

# Method 2: Using callback
def callback(err, result):
    if err:
        print(f"Error: {err}")
    else:
        # Process the result
        print(f"Message type: MT{result['block2']['msg_type']}")
        print(f"Reference: {result['block4']['fields'][0]['fieldValue']}")

# Parse with callback
parser.parse(swift_message, callback)
```

### 6. Database Integration

```python
import sqlite3
from swift_parser_py.swift_parser import SwiftParser

def store_messages_in_db(messages_directory, db_path):
    # Initialize parser and database
    parser = SwiftParser()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS swift_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        msg_type TEXT,
        reference TEXT,
        amount TEXT,
        currency TEXT,
        sender TEXT,
        receiver TEXT,
        raw_message TEXT,
        parsed_data TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Process messages and store in database
    for filename in os.listdir(messages_directory):
        if filename.endswith('.txt'):
            with open(os.path.join(messages_directory, filename), 'r') as file:
                swift_message = file.read()

            try:
                result = parser.process(swift_message)

                # Extract key fields
                msg_type = result['block2']['msg_type']
                reference = result['block4']['fields'][0]['fieldValue']  # Field 20

                # These fields might not exist in all messages
                amount = None
                currency = None
                for field in result['block4']['fields']:
                    if field['type'] == '32' and field.get('option') == 'A':
                        amount = field['ast'].get('Amount')
                        currency = field['ast'].get('Currency')
                        break

                sender = result['block1']['receiving_lt_id']
                receiver = result['block2']['bic']

                # Store in database
                cursor.execute(
                    "INSERT INTO swift_messages (msg_type, reference, amount, currency, sender, receiver, raw_message, parsed_data) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (msg_type, reference, amount, currency, sender, receiver, swift_message, json.dumps(result))
                )

            except Exception as e:
                print(f"Error processing {filename}: {e}")

    # Commit changes and close connection
    conn.commit()
    conn.close()
```

### 7. Integration with Web Applications

#### Flask API Example

```python
from flask import Flask, request, jsonify
from swift_parser_py.swift_parser import SwiftParser

app = Flask(__name__)
parser = SwiftParser()

@app.route('/parse', methods=['POST'])
def parse_message():
    if 'message' not in request.json:
        return jsonify({'error': 'No message provided'}), 400

    swift_message = request.json['message']
    try:
        result = parser.process(swift_message)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

#### Django Integration

```python
# In views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from swift_parser_py.swift_parser import SwiftParser

parser = SwiftParser()

@csrf_exempt
def parse_swift_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if 'message' not in data:
                return JsonResponse({'error': 'No message provided'}, status=400)

            swift_message = data['message']
            result = parser.process(swift_message)
            return JsonResponse(result)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)
```

### 8. Integration with Message Queues

```python
import json
import pika
from swift_parser_py.swift_parser import SwiftParser

# Initialize the parser
parser = SwiftParser()

# Set up RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='swift_messages')
channel.queue_declare(queue='parsed_messages')

def callback(ch, method, properties, body):
    try:
        # Parse the message
        swift_message = body.decode('utf-8')
        result = parser.process(swift_message)

        # Publish the parsed result to another queue
        channel.basic_publish(
            exchange='',
            routing_key='parsed_messages',
            body=json.dumps(result)
        )

        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        # Handle error
        print(f"Error processing message: {e}")
        # Reject the message (could be requeued if needed)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

# Start consuming messages
channel.basic_consume(queue='swift_messages', on_message_callback=callback)
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
```

### 9. Parallel Processing with Multiprocessing

For processing large volumes of messages:

```python
import multiprocessing
from swift_parser_py.swift_parser import SwiftParser
import os
import json

def process_file(file_path):
    try:
        parser = SwiftParser()
        with open(file_path, 'r') as file:
            swift_message = file.read()
        result = parser.process(swift_message)
        return {'file': file_path, 'result': result}
    except Exception as e:
        return {'file': file_path, 'error': str(e)}

def parallel_process_messages(message_dir, output_dir, num_processes=None):
    # Get all message files
    file_paths = [os.path.join(message_dir, f) for f in os.listdir(message_dir) if f.endswith('.txt')]

    # Use multiprocessing to parse messages in parallel
    with multiprocessing.Pool(processes=num_processes or multiprocessing.cpu_count()) as pool:
        results = pool.map(process_file, file_paths)

    # Process results
    for item in results:
        if 'error' in item:
            print(f"Error processing {item['file']}: {item['error']}")
        else:
            # Save parsed result to JSON file
            output_file = os.path.join(output_dir, os.path.basename(item['file']).replace('.txt', '.json'))
            with open(output_file, 'w') as f:
                json.dump(item['result'], f, indent=2)
            print(f"Processed {item['file']} -> {output_file}")
```

## Testing

The project includes comprehensive tests in the `tests` directory:

```python
# Run all tests
python -m unittest discover -s swift_parser_py/tests

# Run specific test files
python -m unittest swift_parser_py.tests.test_block3_parser
python -m unittest swift_parser_py.tests.test_patterns
python -m unittest swift_parser_py.tests.test_comprehensive
```

Sample test output:

```
=== SWIFT MESSAGE PARSING RESULTS ===

BLOCK 1 (BASIC HEADER):
  Application ID: F
  Service ID: 01
  Receiving LT ID: EXAMPLEBANK0
  Session Number: 0010
  Sequence Number: 00001

BLOCK 2 (APPLICATION HEADER):
  Message Type: MT103
  Direction: I
  BIC: RECEIVERBA
  Priority: N

BLOCK 3 (USER HEADER):
  Tag 108: MSGREF2023
  Tag 121: REF-XYZ-789

BLOCK 4 (TEXT BLOCK):
  Field 20: CUSTREF2023-001
  Field 23B: CRED
  Field 32A: 230803USD5000,00
  Field 33B: USD5000,00
  Field 50K: /87654321...
  Field 52A: ORDERBANK
  Field 53A: SENDERBANK
  Field 57A: RECEIVERBANK
  Field 59: /12345678...
  Field 70: PAYMENT FOR SERVICES...
  Field 71A: SHA
  Field 72: /ACC/INTERNAL TRANSFER
```

The test suite includes:
* Tests for various message types (MT103, MT940, MT202, etc.)
* Tests for messages with and without Block 3
* Tests for complex nested blocks and multi-line fields
* Tests for structured fields like 50K and 59
* Tests for field pattern parsing
* Tests for error handling and edge cases

## Contributing

Contributions are welcome! If you'd like to contribute, please:

1. Fork the repository
2. Create a feature branch
3. Add your changes and tests
4. Submit a pull request

## Advanced Features

### 10. Custom Field Patterns

```python
import json
from swift_parser_py.swift_parser import SwiftParser

# Load custom patterns
with open('custom_patterns.json', 'r') as file:
    custom_patterns = json.load(file)

# Initialize parser with custom patterns
parser = SwiftParser(field_patterns=custom_patterns)
```

### 11. Message Validation

```python
from swift_parser_py.swift_parser import SwiftParser

def validate_swift_message(swift_message):
    parser = SwiftParser()
    validation_errors = []

    try:
        result = parser.process(swift_message)

        # Check for required fields
        required_fields = ['20', '23B', '32A', '50K', '59']
        found_fields = [field['type'] for field in result['block4']['fields']]

        for field in required_fields:
            if field not in found_fields:
                validation_errors.append(f"Missing required field: {field}")

        # Check for field parsing errors
        for field in result['block4']['fields']:
            if 'ast' in field and 'error' in field['ast']:
                validation_errors.append(f"Field {field['type']}{field.get('option', '')} parsing error: {field['ast']['error']}")

        # Validate specific fields
        for field in result['block4']['fields']:
            if field['type'] == '32' and field.get('option') == 'A':
                # Validate date format
                date = field['ast'].get('Date', '')
                if len(date) != 6:
                    validation_errors.append(f"Invalid date format in field 32A: {date}")

                # Validate currency code
                currency = field['ast'].get('Currency', '')
                if len(currency) != 3:
                    validation_errors.append(f"Invalid currency code in field 32A: {currency}")

        return {
            'valid': len(validation_errors) == 0,
            'errors': validation_errors,
            'parsed_data': result
        }

    except Exception as e:
        return {
            'valid': False,
            'errors': [f"Error parsing message: {str(e)}"],
            'parsed_data': None
        }
```

## Future Enhancements

Potential areas for future development:
* Message validation against ISO 15022 standards
* Message generation capabilities
* Support for additional message types and field formats
* Performance optimizations for large message volumes
* Integration with message queues and event-driven architectures

## License

Licensed under the MIT License. See [LICENSE](LICENSE) for more information.
