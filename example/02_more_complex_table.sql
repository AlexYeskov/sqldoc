/*
DROP TABLE IF EXISTS example.more_complex_table CASCADE;
CREATE TABLE example.more_complex_table (

	-- IDs
	 id int							-- system ID
	,code text						-- business ID

	-- dimensions
	,country text
	,city text
	,neighborhood text

	-- details
	,full_name text
	,email text

	-- measures
	,revenue_total numeric(10,2)	-- lifetime revenue
	,revenue_monthly numeric(10,2)	-- average monthly revenue over the entire subscription period

);
*/

INSERT INTO example.more_complex_table
VALUES (1,'xxx-123','USA','San Francisco','Mission Bay','John Doe','johndoe@gmail.com',1000,100);