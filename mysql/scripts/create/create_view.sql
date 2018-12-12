CREATE OR REPLACE VIEW v_category(category) AS SELECT DISTINCT category FROM tb_f10 WHERE category <> '';
