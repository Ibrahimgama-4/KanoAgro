# Database setup (Supabase)
Run in the Supabase SQL editor, in order: `0001_core.sql`, `0002_features.sql`, `0003_reference_crops.sql`.
To make yourself an admin (after signing up): 
`insert into user_roles (user_id, role) values ('<your auth user id>', 'admin');`
Deviation from the original spec: irrigation, fertilizer, harvest and treatment records are stored as kinds in
`farm_observations` instead of separate tables; diseases/pests reference content lives in `kanofarm/knowledge/`
until verified sources exist for a database table.
