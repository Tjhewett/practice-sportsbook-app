ALTER TABLE `gridiron_wager`.`%s`
ADD INDEX `%s_fk_idx` (`snapshot_id` ASC) VISIBLE;

ALTER TABLE `gridiron_wager`.`%s`
ADD CONSTRAINT `%s_fk`
  FOREIGN KEY (`snapshot_id`)
  REFERENCES `gridiron_wager`.`snapshots` (`id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
