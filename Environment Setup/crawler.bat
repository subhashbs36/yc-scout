@echo off
REM Batch file to run the web crawler and scraper with parameters

REM Initialize log file
set LOG_FILE=crawler_log.txt
echo Starting the crawler... > %LOG_FILE%
echo %DATE% %TIME%: Starting the batch script >> %LOG_FILE%

:: Activate Python virtual environment (adjust the path as necessary)
echo Activating Python virtual environment...
call venv\Scripts\activate
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to activate virtual environment.
    exit /b 1
)

REM Default values
set OUTPUT_DIR=../output.jl
set SEED_FILE=
set IMAGE_FLAG=0

REM Parse command line arguments
:parse_args
IF "%~1"=="" GOTO done_parsing
IF /I "%~1"=="-o" (
    set OUTPUT_DIR=../%~2
    echo Output directory set to: %OUTPUT_DIR% >> %LOG_FILE%
    echo [INFO] Output directory set to: %OUTPUT_DIR%
    SHIFT
    SHIFT
    GOTO parse_args
)
IF /I "%~1"=="-s" (
    set SEED_FILE=%~2
    echo Seed file set to: %SEED_FILE% >> %LOG_FILE%
    echo [INFO] Seed file set to: %SEED_FILE%
    SHIFT
    SHIFT
    GOTO parse_args
)
IF /I "%~1"=="-i" (
    set IMAGE_FLAG=1
    echo Image data is required. >> %LOG_FILE%
    echo [INFO] Image data is required.
    SHIFT
    GOTO parse_args
)
echo [ERROR] Unknown argument %1 >> %LOG_FILE%
echo [ERROR] Unknown argument %1
exit /b 1

:done_parsing

REM Check if seed.txt file is provided or not
IF "%SEED_FILE%"=="" (
    REM No seed.txt provided, check if image argument is passed
    IF "%IMAGE_FLAG%"=="1" (
        echo [INFO] No seed.txt provided. Running yc_links_extractor_with_image.py to fetch URLs with images...
        echo [INFO] No seed.txt provided. Running yc_links_extractor_with_image.py to fetch URLs with images... >> %LOG_FILE
        REM Run yc_links_extractor_with_image.py to fetch company URLs with image data
        python yc_links_extractor_with_image.py
        IF %ERRORLEVEL% NEQ 0 (
            echo [ERROR] Failed to run yc_links_extractor_with_image.py >> %LOG_FILE
            echo [ERROR] Failed to run yc_links_extractor_with_image.py
            exit /b 1
        )
        
        REM Step 2: Change directory to ycombinator_with_image folder
        cd ycombinator_with_image
        echo [INFO] Changed directory to ycombinator_with_image >> %LOG_FILE
        echo [INFO] Changed directory to ycombinator_with_image

        REM Step 3: Run Scrapy spider to scrape the company details with images
        echo [INFO] Running Scrapy spider to scrape the companies with images...
        REM Delete old output file if it exists
        IF EXIST "%OUTPUT_DIR%" (
            echo [INFO] Existing output file found. Deleting %OUTPUT_DIR%...
            del "%OUTPUT_DIR%"
            echo [INFO] Output file deleted.
        )
        scrapy runspider ycombinator/spiders/yscraper.py -o %OUTPUT_DIR%
        IF %ERRORLEVEL% NEQ 0 (
            echo [ERROR] Scrapy spider failed during image scraping >> %LOG_FILE
            echo [ERROR] Scrapy spider failed during image scraping
            exit /b 1
        )
        echo [INFO] Scrapy spider finished successfully for image scraping.

    ) ELSE (
        REM No image argument, just run the normal extractor
        echo [INFO] No seed.txt provided. Running yc_links_extractor.py to fetch URLs without images...
        echo [INFO] No seed.txt provided. Running yc_links_extractor.py to fetch URLs without images... >> %LOG_FILE
        REM Run yc_links_extractor.py to fetch company URLs without image data
        python yc_links_extractor.py
        IF %ERRORLEVEL% NEQ 0 (
            echo [ERROR] Failed to run yc_links_extractor.py >> %LOG_FILE
            echo [ERROR] Failed to run yc_links_extractor.py
            exit /b 1
        )

        REM Step 2: Change directory to ycombinator folder
        cd ycombinator
        echo [INFO] Changed directory to ycombinator >> %LOG_FILE
        echo [INFO] Changed directory to ycombinator

        REM Step 3: Run Scrapy spider to scrape the company details without images
        echo [INFO] Running Scrapy spider to scrape the companies without images...
        IF EXIST "%OUTPUT_DIR%" (
            echo [INFO] Existing output file found. Deleting %OUTPUT_DIR%...
            del "%OUTPUT_DIR%"
            echo [INFO] Output file deleted.
        )
        scrapy runspider ycombinator/spiders/yscraper.py -o %OUTPUT_DIR%
        IF %ERRORLEVEL% NEQ 0 (
            echo [ERROR] Scrapy spider failed during non-image scraping >> %LOG_FILE
            echo [ERROR] Scrapy spider failed during non-image scraping
            exit /b 1
        )
        echo [INFO] Scrapy spider finished successfully for non-image scraping.
    )
) ELSE (
    REM Seed.txt provided, copying and renaming it...
    echo [INFO] Seed.txt provided, copying and renaming it... >> %LOG_FILE
    echo [INFO] Seed.txt provided, copying and renaming it...

    REM Skip the extractor script since seed.txt is provided
    REM Check if 'image' is the argument
    IF "%IMAGE_FLAG%"=="1" (
        REM If image required, copy seed.txt to ycombinator_with_image directory
        echo [INFO] Copying "%SEED_FILE%" to ycombinator_with_image/ycombinator/start_urls.txt...
        copy "%SEED_FILE%" "ycombinator_with_image/ycombinator/start_urls.txt"
        
        REM Change directory to ycombinator_with_image folder
        cd ycombinator_with_image
        echo [INFO] Changed directory to ycombinator_with_image >> %LOG_FILE
        echo [INFO] Changed directory to ycombinator_with_image

        REM Run Scrapy spider to scrape company details including images
        echo [INFO] Running Scrapy spider to scrape companies with images...
        IF EXIST "%OUTPUT_DIR%" (
            echo [INFO] Existing output file found. Deleting %OUTPUT_DIR%...
            del "%OUTPUT_DIR%"
            echo [INFO] Output file deleted.
        )
        scrapy runspider ycombinator/spiders/yscraper.py -o %OUTPUT_DIR%
        IF %ERRORLEVEL% NEQ 0 (
            echo [ERROR] Scrapy spider failed during image scraping >> %LOG_FILE
            echo [ERROR] Scrapy spider failed during image scraping
            exit /b 1
        )
        echo [INFO] Scrapy spider finished successfully for image scraping.

    ) ELSE (
        REM If no 'image' argument, copy seed.txt to ycombinator directory
        echo [INFO] Copying "%SEED_FILE%" to ycombinator/ycombinator/start_urls.txt...
        copy "%SEED_FILE%" "ycombinator/ycombinator/start_urls.txt"
        
        REM Change directory to ycombinator folder
        cd ycombinator
        echo [INFO] Changed directory to ycombinator >> %LOG_FILE
        echo [INFO] Changed directory to ycombinator

        REM Run Scrapy spider to scrape the company details without images
        echo [INFO] Running Scrapy spider to scrape the companies without images...
        IF EXIST "%OUTPUT_DIR%" (
            echo [INFO] Existing output file found. Deleting %OUTPUT_DIR%...
            del "%OUTPUT_DIR%"
            echo [INFO] Output file deleted.
        )
        scrapy runspider ycombinator/spiders/yscraper.py -o %OUTPUT_DIR%
        IF %ERRORLEVEL% NEQ 0 (
            echo [ERROR] Scrapy spider failed during non-image scraping >> %LOG_FILE
            echo [ERROR] Scrapy spider failed during non-image scraping
            exit /b 1
        )
        echo [INFO] Scrapy spider finished successfully for non-image scraping.
    )
)
REM Change directory back to the previous directory
cd ..
echo [INFO] Changed back to the previous directory.

REM End
echo [INFO] Crawler finished! Results saved to %OUTPUT_DIR%. >> %LOG_FILE
echo [INFO] Crawler finished! Results saved to %OUTPUT_DIR%.
pause
