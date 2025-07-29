from croustiistuff.logger import Logger

if __name__ == "__main__":
    logger = Logger(prefix="MyApp")

    # Custom with hex color
    logger.custom(symbol="✦", title="Solved", message="Custom log with hex color!", color="#9D26FF", in_="Alice")

    # Custom with ANSI named color
    logger.custom(symbol="€", title="ALERT", message="Alert message here", color=logger.colors['warning'])

    # Old methods still work exactly the same
    logger.success("Operation completed successfully")
    logger.error("Something went wrong")
    logger.info("Informational message")
