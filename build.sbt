name := "template_cicd_scala"

version := "1.0"

scalaVersion := "2.11.12"

val TYPESAFE_CONFIG_VERSION = "1.3.3"

libraryDependencies ++= Seq(
  "com.typesafe" % "config" % TYPESAFE_CONFIG_VERSION,
  "org.slf4j" % "slf4j-log4j12" % "1.2"
)