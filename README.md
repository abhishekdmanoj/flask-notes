# Flask Notes

It's a Dockerized notes application made using Flask with user authentication, PostgreSQL, automated testing with Pytest, and Continuous Integration using GitHub Actions - my first attempt at a fully containerized application using multiple containers with real world utility.

Honestly, it was much more fun and interesting than I thought it would be - who would've thought it? Real world projects are much more fun than disappearing down the LeetCode rabbit hole. xd

# Features

- User registration
- Secure password hashing
- User login/logout
- Session-based authentication
- Full CRUD Operations for notes
- PostgreSQL database
- Flash messages
- Automated integration testing with Pytest
- Continuous Integration using GitHub Actions
- Fully Dockerized using Docker Compose
- Environment variable configuration

# Tech Stack

| Technology     | Purpose                                |
| -------------- | -------------------------------------- |
| Python         | Programming language                   |
| Flask          | Backend web framework                  |
| PostgreSQL     | Relational database                    |
| Docker         | Containerization                       |
| Docker Compose | Multi-container orchestration          |
| Pytest         | Automated integration testing          |
| GitHub Actions | Continuous Integration (CI)            |
| AWS EC2        | Development and deployment environment |
| HTML           | Frontend templates                     |
| CSS            | Application styling                    |
| Werkzeug       | Password hashing and authentication    |

# Structure

```text
flask-notes/
│
├── app.py
├── config.py
├── database.py
├── helpers.py
├── notes.py
├── users.py
├── routes_auth.py
├── routes_notes.py
│
├── templates/
├── static/
├── tests/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

# HOW TO USE

## Getting Started
### Prerequisites

- Git
- Docker
- Docker Compose

### Clone the repository

```bash
git clone https://github.com/abhishekdmanoj/flask-notes.git
cd flask-notes
```

### Configure environment variables

Create a `.env` file from the provided example.

```bash
cp .env.example .env
```

Update the values in `.env` to match your PostgreSQL configuration and generate a secure `SECRET_KEY`.

### Build the Flask image

Build the Flask image before starting the application:

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

### Running the tests

With the application running, execute:

```bash
docker compose exec flask pytest
```

### To stop the application

```bash
docker compose down
```

# What I Learned

Apparently this section is a thing.

Building this helped me gain experience with:

- Docker and Docker Compose
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
- Continuous Deployment using GitHub Actions
- Deploy using Gunicorn and Nginx

## License

This project is licensed under the MIT License.

# Screenshots

- Coming Soon

# Afterthoughts

If you made it this far, congratulations! Here's a cookie for you. 🍪
It's crazy how much more fun programming becomes when you can apply it to solve a real world problem.
Somewhere along the way I realized I'm more fascinated by everything that happens around the code, rather than the code itself - HTTP, Container interaction, deployment, CI/CD, catch my groove?
