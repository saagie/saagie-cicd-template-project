package spark

import com.typesafe.config.{Config, ConfigFactory}
import org.slf4j.{Logger, LoggerFactory}

object template_test_2 {
  val config: Config = ConfigFactory.load()
  val logger: Logger = LoggerFactory.getLogger(getClass)
  logger.info("hello world 2")
}