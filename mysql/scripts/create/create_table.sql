CREATE TABLE `tb_f10` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    `stockcode` INT(11) NOT NULL,
    `category` VARCHAR(16) NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
    `content` LONGTEXT NULL COLLATE 'utf8mb4_unicode_ci',
    PRIMARY KEY (`id`)
)
COLLATE='utf8mb4_unicode_ci'
CHARACTER SET utf8mb4
ENGINE=InnoDB
;


CREATE FULLTEXT INDEX ngram_idx ON tb_f10(content) WITH PARSER ngram;

