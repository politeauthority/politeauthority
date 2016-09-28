CREATE TABLE `people` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`voter_id` INT(12) DEFAULT NULL,
	`county_code` INT(12) DEFAULT NULL,
	`county` VARCHAR(64) DEFAULT NULL,
	`last_name` VARCHAR(256) DEFAULT NULL,
	`first_name` VARCHAR(256) DEFAULT NULL, 
	`middle_name` VARCHAR(256) DEFAULT NULL, 
	`name_suffix` VARCHAR(50) DEFAULT NULL, 
	`voter_name` VARCHAR(256) DEFAULT NULL, 
	`status_code` VARCHAR(2)  DEFAULT NULL,
	`precinct_name` VARCHAR(20) DEFAULT NULL,
	`address_library_id` VARCHAR(20) DEFAULT NULL,
	`house_num`  VARCHAR(40) DEFAULT NULL,
	`house_suffix` VARCHAR(40) DEFAULT NULL,
	`pre_dir` VARCHAR(40) DEFAULT NULL,
	`street_name` VARCHAR(256) DEFAULT NULL,
	`street_type` VARCHAR(256) DEFAULT NULL,
	`post_dir` VARCHAR(40) DEFAULT NULL,
	`unit_type` VARCHAR(40) DEFAULT NULL,
	`unit_num` VARCHAR(40) DEFAULT NULL,
	`address_non_std` VARCHAR(40) DEFAULT NULL,
	`residential_address` VARCHAR(256) DEFAULT NULL,
	`residential_city` VARCHAR(256) DEFAULT NULL,
	`residential_state` VARCHAR(10) DEFAULT NULL,
	`residential_zip_code` VARCHAR(10) DEFAULT NULL,
	`residential_zip_plus` VARCHAR(10)DEFAULT NULL,
	`effective_date` DATETIME DEFAULT NULL,
	`registration_date` DATETIME DEFAULT NULL,
	`status` VARCHAR(10) DEFAULT NULL,
	`status_reason` VARCHAR(60) DEFAULT NULL,
	`birth_year` INT(4) DEFAULT NULL,
	`gender` VARCHAR(10) DEFAULT NULL,
	`precinct` VARCHAR(60) DEFAULT NULL,
	`split`  VARCHAR(60) DEFAULT NULL,
	`voter_status_id` INT(10) DEFAULT NULL,
	`party` VARCHAR(10) DEFAULT NULL,
	`party_affiliation_date` DATETIME DEFAULT NULL,
	`phone_num` TEXT DEFAULT NULL,
	`mail_addr1` VARCHAR(255) DEFAULT NULL,
	`mail_addr2` VARCHAR(255) DEFAULT NULL,
	`mail_addr3` VARCHAR(255) DEFAULT NULL,
	`mailing_city` VARCHAR(255) DEFAULT NULL,
	`mailing_state` VARCHAR(10) DEFAULT NULL,
	`mailing_zip_code` VARCHAR(8) DEFAULT NULL,
	`mailing_zip_plus` VARCHAR(5) DEFAULT NULL,
	`mailing_country` VARCHAR(200) DEFAULT NULL,
	`spl_id`  VARCHAR(10) DEFAULT NULL,
	`permanent_mail_in_voter` VARCHAR(200) DEFAULT NULL,
	`congressional` VARCHAR(200) DEFAULT NULL,
	`state_senate` VARCHAR(200) DEFAULT NULL,
	`state_house`VARCHAR(200) DEFAULT NULL, 
	`id_required`VARCHAR(200) DEFAULT NULL,
	PRIMARY KEY ( id )
);