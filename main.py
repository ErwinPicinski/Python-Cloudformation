import boto3

import aws_settings


def connect_aws():
    # Connect to aws using connection params from aws_settings.py
    try: 
        aws_cloudformation_client = boto3.client('cloudformation', 
                      aws_access_key_id=aws_settings.ACCESS_KEY_ID, 
                      aws_secret_access_key=aws_settings.SECCRET_KEY, 
                      region_name=aws_settings.REGION
        )
    except:
        print("Connection failed")

    return aws_cloudformation_client


def get_template(template_path):
    # Read template.json 

    template = ''
    
    try:
        with open(f"{template_path}/template.json", 'r') as f: # Open file and get data
            template = f.read()
    except:
        print("Failed to load file")

    return template


if __name__ == "__main__":
    # Get params and path

    template = get_template(input("Template path:"))
    stack_name = input("Stack name: ").replace(" ", "")
    policy_name = input("Policy name: ").replace(" ", "")
    
    parameters = [
        {
            'ParameterKey': 'RoleName',
            'ParameterValue': policy_name
        }
    ]
    
    aws = connect_aws()

    try: # Try to create new stack 
        aws.create_stack(StackName=stack_name,
                     TemplateBody=template,
                     Capabilities=['CAPABILITY_NAMED_IAM'],
                     Parameters=parameters
                     )
    except:
        print("Can't create new stack")

    print(aws.describe_stacks())