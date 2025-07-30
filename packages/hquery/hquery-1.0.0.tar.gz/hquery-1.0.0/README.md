# .h.sql

```sql
-- main.h.sql

-- This is the head section
head:
CREATE title CONTAINS "example site" WITH (ID = "title") 
CREATE script WITH (SRC = "https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4")
body:
-- This is a body comment
CREATE div CONTAINS (
    CREATE h1 CONTAINS "1"
    CREATE h2 CONTAINS "2"
)
END
```

```bash
hquery </path/to/your/file.h.sql> --ofuscate <type>
```

ofuscation types:
* minify
* hex
* base64
* charcode

for no ofuscations use
```bash
hquery </path/to/your/file.h.sql>
```