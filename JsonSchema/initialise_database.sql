CREATE EXTENSION IF NOT EXISTS dblink;

-- Check if the database 'jsonschema' exists
DO $$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'jsonschema') THEN
      -- Create the database 'jsonschema'
      PERFORM dblink_exec('dbname=postgres', 'CREATE DATABASE jsonschema');
   END IF;
END
$$;

-- Connect to the 'jsonschema' database to create the user and assign roles
-- Switch to the jsonschema database
\c jsonschema;

-- Check if the user 'mayank' exists
DO $$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'mayank') THEN
      -- Create the user 'mayank' with the specified password
      CREATE USER mayank WITH PASSWORD '*password@#';
      -- Grant the user 'mayank' the 'admin' role
      ALTER USER mayank WITH SUPERUSER;
   END IF;
END
$$;
