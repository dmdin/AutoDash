ALTER TABLE "savedTemplates" DROP CONSTRAINT "savedTemplates_templateId_templates_id_fk";
--> statement-breakpoint
ALTER TABLE "savedTemplates" ADD COLUMN "body" text NOT NULL;--> statement-breakpoint
ALTER TABLE "savedTemplates" ADD COLUMN "authorId" text NOT NULL;--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "savedTemplates" ADD CONSTRAINT "savedTemplates_authorId_user_id_fk" FOREIGN KEY ("authorId") REFERENCES "user"("id") ON DELETE no action ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
ALTER TABLE "savedTemplates" DROP COLUMN IF EXISTS "templateId";