CREATE TABLE IF NOT EXISTS "sources" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"title" text NOT NULL,
	"link" text NOT NULL
);
