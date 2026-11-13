# Local Pages engine smoke test

1. Add a Django test covering sign-in, a directory link, and protected HTML on a separate Page hostname.
2. Run it before adding the directory and Page routes. Implement the routes with Django sessions and one SQLite database. Use a checked-in sample with no repository credentials.
3. Add a Docker Compose launch and document the commands for a clean checkout. Verify the test suite, render the sample in Chrome, and record which deployment checks remain.
