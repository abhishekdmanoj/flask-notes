# Flask Notes

Its a Dockerized notes application made using Flask with user authentication and PostgreSQL - my first attempt at a fully containerized application using multiple containers.

Honestly, it was much more fun and interesting than I thought it would be - who would've thought it? Real world projects are much more fun than disappearing down the LeetCode rabbit hole. xd

#Features

- User registration
- Fully secure password hashing
- User login and logout
- Session based auth
- CRUD operations for notes
- PostgreSQL as database
- Flash messages for clarity of operations
- Fully Dockerized using Docker Compose
- Environment variable configuration for security

# Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Programming language |
| Flask | Web framework |
| PostgreSQL | Database |
| Docker | Containerization |
| Docker Compose | Multi-container orchestration |
| HTML | Frontend templates |

# Structure

flask-notes/
│
├── app.py
├── database.py
├── helpers.py
├── notes.py
├── users.py
│
├── templates/
├── static/
│
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── .env.example
└── README.md

# HOW TO USE

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Clone the repository

```bash
git clone https://github.com/<your-username>/flask-notes.git
cd flask-notes
```

### Configure environment variables

Create a `.env` file from the provided example.

```bash
cp .env.example .env
```

Update the values in `.env` to match your PostgreSQL configuration and generate a secure `SECRET_KEY`.

### Build the Flask image

If your `compose.yaml` uses `image: flask-notes`, build the image first:

```bash
docker build -t flask-notes .
```

### Start the application

```bash
docker compose up
```

### Access the application

Open your browser and navigate to:

```
http://localhost:5000
```

To stop the application:

```bash
docker compose down
```

# What I Learned

Apparently its a thing.

Building this helped me gain experience with:

- Docker and Docker commpose
- Flask application architecture
- PostgreSQL integration using psycopg2
- Session based auth
- Password hashing using Werkzeug
- CRUD Operations in Postgres
- Environment variable management and why they're needed
- Git and GitHub workflow(I've used this before, but yeah I was rusty)
- Developing inside an AWS EC2 environment(This project started out with me fiddling around with AWS EC2 Instances)

# FUTURE ENHANCEMENTS

## Future Improvements

- Convert the backend into a REST API
- Build a React frontend
- JWT authentication
- Automated testing
- CI/CD with GitHub Actions
- Deploy using Gunicorn and Nginx

## License

This project is licensed under the MIT License.

# Screenshots

- Coming Soon

# Afterthoughts

If you made it this far, congratulations! Here's a cookie for you. 🍪
It's crazy how much more fun programming becomes when you can apply it to solve a real world problem.
Somewhere along the way I realized I'm more fascinated by everything that happens around the code, rather than the code itself - HTTP, Container interaction, deployment, CI/CD, catch my groove?
