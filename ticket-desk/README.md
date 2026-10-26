# Ticket desk

## Database

The desk's MySQL server runs in a Docker container. Create the container once:

    docker run --name desk-mysql -e MYSQL_ROOT_PASSWORD=desk -p 3306:3306 -v desk-data:/var/lib/mysql -d mysql:9.7

- `--name desk-mysql` names the container, so every later command can find it.
- `-e MYSQL_ROOT_PASSWORD=desk` sets the password of the database's root user on the first start.
- `-p 3306:3306` connects port 3306 on the laptop to port 3306 inside the container.
- `-v desk-data:/var/lib/mysql` keeps the database files in the volume `desk-data`, outside the container.
- `-d` runs the container in the background and gives the terminal back.

Open the mysql client inside the container, and type the password `desk` at the prompt:

    docker exec -it desk-mysql mysql -uroot -p

After a reboot, start the same container again with `docker start desk-mysql`.

Build the desk's database and its tables from `ticket-desk/`:

    docker exec -i desk-mysql mysql -uroot -pdesk < sql/schema.sql
