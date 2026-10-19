from datetime import timedelta
from desk import NOW, Desk, Ticket

def main():
    """This method will act as the entrypoint of my application"""
    t1 = Ticket(1, "Login page returns 500", "high", NOW - timedelta(hours=30))
    t2 = Ticket(2, "Invoice PDF is blank", "normal", NOW - timedelta(hours=50))
    t3 = Ticket(3, "Typo on pricing page", "normal", NOW - timedelta(hours=20))
    t4 = Ticket(4, "Add dark mode", "low", NOW - timedelta(hours=26))

    tickets = [t1, t2, t3, t4]

    t1.close(t1.opened_at + timedelta(hours=3))
    t3.close(t3.opened_at + timedelta(hours = 10))

    t2.assign("Marco")
    t4.assign("Jonathan")

    desk = Desk() # create a Desk object

    for t in tickets:
        print(t.ticket_id, t.priority, t.status, t.days_open())
        desk.add(t) # adding ticket to my desk

    print(desk.overdue())
    
# This is what actually runs our application
if __name__ == "__main__":
    main()
