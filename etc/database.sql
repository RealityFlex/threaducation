

CREATE TABLE post_table (
  post_id bigint NOT NULL PRIMARY KEY,
  content char NOT NULL,
  child_id bigint,
  user_id bigint NOT NULL,
  media_link char,
  creation_date date NOT NULL,
  views_count bigint NOT NULL,
  post_type_id bigint NOT NULL
);


CREATE TABLE tags_for_post_table (
  id bigint NOT NULL PRIMARY KEY,
  post_id bigint NOT NULL,
  tag_id bigint NOT NULL
);


CREATE TABLE tag_type_table (
  tag_type_id bigint NOT NULL PRIMARY KEY,
  name char NOT NULL
);


CREATE TABLE like_table (
  like_id bigint NOT NULL PRIMARY KEY,
  post_id bigint NOT NULL,
  user_id bigint NOT NULL
);


CREATE TABLE tag_table (
  tag_id bigint NOT NULL PRIMARY KEY,
  name char NOT NULL,
  tag_type_id bigint NOT NULL
);


CREATE TABLE tags_for_user_table (
  id bigint NOT NULL PRIMARY KEY,
  user_id bigint NOT NULL,
  tag_id bigint NOT NULL
);


CREATE TABLE change_request_table (
  change_request_id bigint NOT NULL PRIMARY KEY,
  description char NOT NULL,
  from_id bigint NOT NULL,
  program_id bigint NOT NULL
);


CREATE TABLE user_table (
  user_id bigint NOT NULL PRIMARY KEY,
  login char NOT NULL,
  password char NOT NULL,
  type_id bigint NOT NULL,
  name char NOT NULL,
  image_link char,
  description char,
  rating real NOT NULL
);


CREATE TABLE profile_type_table (
  type_id bigint NOT NULL PRIMARY KEY,
  name char NOT NULL
);


CREATE TABLE education_program_table (
  program_id bigint NOT NULL PRIMARY KEY,
  user_id bigint NOT NULL,
  code bigint NOT NULL,
  name bigint NOT NULL,
  time bigint NOT NULL,
  education_type_id bigint NOT NULL,
  description char NOT NULL,
  quota bigint NOT NULL
);


CREATE TABLE learning_plan_table (
  id bigint NOT NULL PRIMARY KEY,
  program_id bigint NOT NULL,
  subject_id bigint NOT NULL,
  hours bigint NOT NULL,
  semester bigint NOT NULL
);


CREATE TABLE subject_table (
  subject_id bigint NOT NULL PRIMARY KEY,
  name char NOT NULL,
  description bigint NOT NULL
);


CREATE TABLE education_type_table (
  education_type_id bigint NOT NULL PRIMARY KEY,
  name char NOT NULL
);


CREATE TABLE post_type_table (
  post_type_id bigint NOT NULL PRIMARY KEY,
  name char NOT NULL
);


ALTER TABLE post_table ADD CONSTRAINT post_table_post_id_fk FOREIGN KEY (post_id) REFERENCES like_table (post_id);
ALTER TABLE post_table ADD CONSTRAINT post_table_post_id_fk FOREIGN KEY (post_id) REFERENCES tags_for_post_table (post_id);
ALTER TABLE tag_type_table ADD CONSTRAINT tag_type_table_tag_type_id_fk FOREIGN KEY (tag_type_id) REFERENCES tag_table (tag_type_id);
ALTER TABLE tag_table ADD CONSTRAINT tag_table_tag_id_fk FOREIGN KEY (tag_id) REFERENCES tags_for_post_table (tag_id);
ALTER TABLE tag_table ADD CONSTRAINT tag_table_tag_id_fk FOREIGN KEY (tag_id) REFERENCES tags_for_user_table (tag_id);
ALTER TABLE tags_for_user_table ADD CONSTRAINT tags_for_user_table_user_id_fk FOREIGN KEY (user_id) REFERENCES user_table (user_id);
ALTER TABLE user_table ADD CONSTRAINT user_table_type_id_fk FOREIGN KEY (type_id) REFERENCES profile_type_table (type_id);
ALTER TABLE user_table ADD CONSTRAINT user_table_user_id_fk FOREIGN KEY (user_id) REFERENCES like_table (user_id);
ALTER TABLE user_table ADD CONSTRAINT user_table_user_id_fk FOREIGN KEY (user_id) REFERENCES change_request_table (from_id);
ALTER TABLE change_request_table ADD CONSTRAINT change_request_table_program_id_fk FOREIGN KEY (program_id) REFERENCES education_program_table (program_id);
ALTER TABLE user_table ADD CONSTRAINT user_table_user_id_fk FOREIGN KEY (user_id) REFERENCES education_program_table (user_id);
ALTER TABLE education_program_table ADD CONSTRAINT education_program_table_program_id_fk FOREIGN KEY (program_id) REFERENCES learning_plan_table (program_id);
ALTER TABLE subject_table ADD CONSTRAINT subject_table_subject_id_fk FOREIGN KEY (subject_id) REFERENCES learning_plan_table (subject_id);
ALTER TABLE education_type_table ADD CONSTRAINT education_type_table_education_type_id_fk FOREIGN KEY (education_type_id) REFERENCES education_program_table (education_type_id);
ALTER TABLE post_type_table ADD CONSTRAINT post_type_table_post_type_id_fk FOREIGN KEY (post_type_id) REFERENCES post_table (post_type_id);
