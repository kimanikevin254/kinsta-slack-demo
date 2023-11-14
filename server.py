import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from db import get_conn, init_db
from psycopg2 import DatabaseError

# Initializes your app with your bot token
app = App(
  token=os.environ.get("SLACK_BOT_TOKEN"),
)

# The hi command simply sends back a greeting
@app.command("/hi")
def send_hello(ack, respond, command):
  # Acknowledge command request
  ack()
  respond(f"Hello!")
# command to add products
@app.command("/add_product")
def add_product(ack, respond, command, request):
 #Acknowledge command request
 ack()

 # Extract payload from request
 payload = request.body['text']
 id, name, quantity = [i.strip() for i in payload.split(",")]
  
 # conn object
 conn = None

 try:
   # get conn
   conn = get_conn()

   # get cursor
   cur = conn.cursor()

   # Insert product into the database
   cur.execute(
     "INSERT INTO products (id, name, quantity) VALUES (%s, %s, %s)",
       (int(id), name, int(quantity))
   )
   
   # close communication with postgresql
   cur.close()
   
   # commit changes
   conn.commit()
   
   # Response
   respond(f"""Added product to inventory:
     id - {id},
     name - {name},
     quantity - {quantity}
   """)

 except DatabaseError:
   # Send a response
   respond(f"Product with ID {id} exists in inventory!")
  
 finally:
   # close connection
   if conn is not None:
     conn.close()

# command to check inventory for a product_id
@app.command("/check_inventory")
def check_inventory(ack, respond, command, request):
   # Acknowledge command request
   ack()

   # Extract payload from request
   id = request.body['text'].strip()

   # Get database connection
   conn = None
   try:
       # get conn
       conn = get_conn()

       # get cursor
       cur = conn.cursor()
 
       # Fetch matching product with ID from database
       cur.execute(
           "SELECT * FROM products WHERE id=%s",
           (int(id),)
       )

       product = cur.fetchone()

       # close comms
       cur.close()

       if product is None:
           respond(f"No product with matching ID {id} found.")
       else:
           # Deconstruct tuple if product exists
           _, name, quantity = product
          
           respond(f"""Product with ID {id} found:
                      name - {name},
                      quantity - {quantity}
                  """)
         
   except Exception as e:
       print("Connection error: %s", e)
         
   finally:
       # close connection
       if conn is not None:
           conn.close()


# command to delete the matching product_id from inventory
@app.command("/delete_product")
def delete_product(ack, respond, command, request):
    #Acknowledge command request
    ack()

    # Extract payload from request
    id = request.body['text'].strip()
    
    # Get connection
    conn = None
    try:
        # Get connection
        conn = get_conn()
   	 
        # get cursor
        cur = conn.cursor()
   	 
        # Insert product into the database
        cur.execute(
        	"DELETE FROM products WHERE id = %s",
        	(int(id),)
        )
        cur.close()
        conn.commit()
   	 
        # Response
        respond(f"Product with ID {id} deleted from inventory!")
    except Exception as e:
        print("Connection error: %s", e)
    finally:
        # close connection
        if conn is not None:
            conn.close()

# Start your app
if __name__ == "__main__":
    # Initialize database on start
    init_db()

    # Connect socket
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()


