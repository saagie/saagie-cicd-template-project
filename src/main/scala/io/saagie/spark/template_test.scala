package io.saagie.spark

import com.typesafe.config.{Config, ConfigFactory}
import org.slf4j.{Logger, LoggerFactory}

object template_test {
  val config: Config = ConfigFactory.load()
  val logger: Logger = LoggerFactory.getLogger(getClass)
  logger.info("hello world 1")
}
