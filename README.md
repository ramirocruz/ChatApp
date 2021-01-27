# SNS ASSIGNMENT 1
## An end to end messaging system like WhatsApp




## Running Instructions:
* For Server : python3 server.py < --- /PORT NO.>
* For Client : python3 client.py <SERVER IP> <SERVER PORT> <IP> <PORT NO.>

## COMMANDS
* create_user   <username>   <password>   ------> CREATES A NEW-USER
* login <username> <password> -------> LOGS IN A USER
* send <username> <message>   -------> sends message to the specified user
* send_file <username> <filepath>   -------> sends file to the specified user
* create_group <groupname>                --------> creates group with the specified name
* join <groupname>   -------->the user joins the specified group
* list_groups  -------->lists the name and the members of the groups
* group_send <gropname> <message>    --------->sends a message to the specified group
* group_send_file <groupname> <filepath>-------->sends a file to the specified group