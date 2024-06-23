ALTER TABLE "blocks" DROP CONSTRAINT "blocks_dashboardId_dashboards_id_fk";
--> statement-breakpoint
ALTER TABLE "prompts" DROP CONSTRAINT "prompts_widgetId_widgets_id_fk";
--> statement-breakpoint
ALTER TABLE "widgets" DROP CONSTRAINT "widgets_blockId_blocks_id_fk";
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "blocks" ADD CONSTRAINT "blocks_dashboardId_dashboards_id_fk" FOREIGN KEY ("dashboardId") REFERENCES "dashboards"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "prompts" ADD CONSTRAINT "prompts_widgetId_widgets_id_fk" FOREIGN KEY ("widgetId") REFERENCES "widgets"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
--> statement-breakpoint
DO $$ BEGIN
 ALTER TABLE "widgets" ADD CONSTRAINT "widgets_blockId_blocks_id_fk" FOREIGN KEY ("blockId") REFERENCES "blocks"("id") ON DELETE cascade ON UPDATE no action;
EXCEPTION
 WHEN duplicate_object THEN null;
END $$;
