
CREATE TABLE "recipe" (
	"id"	TEXT NOT NULL UNIQUE,
	"tag"	TEXT,
	"tag_value"	TEXT,
	PRIMARY KEY("id")
);

CREATE TABLE "ingredient" (
	"id"	TEXT NOT NULL UNIQUE,
	"tag"	TEXT,
	"tag_value"	TEXT,
	PRIMARY KEY("id")
);

CREATE TABLE "instruction" (
	"id"	TEXT NOT NULL UNIQUE,
	"tag"	TEXT,
	"tag_value"	TEXT,
	PRIMARY KEY("id")
);

CREATE TABLE "recipe_ingredient" (
	"recipe_id"	TEXT,
	"ingredient_id"	TEXT
)

CREATE TABLE "recipe_instruction" (
	"recipe_id"	TEXT,
	"instruction_id" TEXT
)