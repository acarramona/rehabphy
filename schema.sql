-- Create a login 'RehabPhyUser' and the password
CREATE LOGIN RehabPhyUser
WITH PASSWORD = 'P@ssw0rd!3863835',
	CHECK_POLICY = ON;

USE rehabphydb;
GO

-- Create a database user linked to the login
CREATE USER RehabPhyUser FOR LOGIN RehabPhyUser;
GO

-- Assign the user to the db_datareader and db_datawriter roles
EXEC sp_addrolemember 'db_datareader', 'RehabPhyUser';
EXEC sp_addrolemember 'db_datawriter', 'RehabPhyUser';
GO

-- Grant EXECUTE permission to allow execution of stored procedures and functions
GRANT EXECUTE TO RehabPhyUser;
GO

-- Grant CREATE TABLE permission to allow the user to create tables
GRANT CREATE TABLE TO RehabPhyUser;
GO

-- Grant REFERENCES permission on the schema to handle foreign key constraints
GRANT REFERENCES ON SCHEMA::dbo TO RehabPhyUser;
GO

-- Grant ALTER permission on the schema incase the changes are made via the 
-- supporting ORM codebase
GRANT ALTER ON SCHEMA::dbo TO RehabPhyUser;
GO