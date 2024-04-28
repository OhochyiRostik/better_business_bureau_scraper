const path = require('path');
const {
  PYTHON_INTERPRETER,
  SCRAPY_SCRIPT,
  PROJECT_PREFIX,
  MAX_MEMORY_RESTART,
  PYTHON_CWD,
  TYPESCRIPT_CWD,
  PM2_LOG_DIRECTORY,
  NODEJS_SCRIPT,
} = require('./settings/settings');

const spiders = [
  {
    name: `${PROJECT_PREFIX}_bbb_url_spider`,
    script: SCRAPY_SCRIPT,
    args: "crawl bbb_url_spider",
    interpreter: PYTHON_INTERPRETER,
    instances: 1,
    autorestart: true,
    cron_restart: "0 0 * * *",
  },
  {
    name: `${PROJECT_PREFIX}_bbb_business_spider`,
    script: SCRAPY_SCRIPT,
    args: "crawl bbb_business_spider",
    interpreter: PYTHON_INTERPRETER,
    instances: 1,
    autorestart: true,
    cron_restart: "0 0 * * *",
  },
];

const producers = [
  {
    name: `${PROJECT_PREFIX}_producer_custom`,
    script: SCRAPY_SCRIPT,
    args: "producer_custom --task_queue=bbb_business_spider_task_queue --reply_to_queue=bbb_business_spider_reply_queue --mode=worker --chunk_size=200",
    interpreter: PYTHON_INTERPRETER,
    instances: 1,
    autorestart: true,
    cron_restart: "0 0 * * *",
  },
];

const consumers = [
  {
    name: `${PROJECT_PREFIX}_consumer_result_queue_custom`,
    script: SCRAPY_SCRIPT,
    args: "consumer_result_queue_custom --queue=bbb_business_spider_result_queue --mode=worker --prefetch_count=100",
    interpreter: PYTHON_INTERPRETER,
    instances: 1,
    autorestart: true,
    cron_restart: "0 0 * * *",
  },
  {
    name: `${PROJECT_PREFIX}_consumer_reply_queue_custom`,
    script: SCRAPY_SCRIPT,
    args: "consumer_reply_queue_custom --queue=bbb_business_spider_reply_queue --mode=worker --prefetch_count=100",
    interpreter: PYTHON_INTERPRETER,
    instances: 1,
    autorestart: true,
    cron_restart: "0 0 * * *",
  },
];

const commands = [
  {
    name: `${PROJECT_PREFIX}_csv_exporter`,
    script: SCRAPY_SCRIPT,
    args: "csv_exporter",
    interpreter: PYTHON_INTERPRETER,
    instances: 1,
    autorestart: true,
    cron_restart: "0 0 * * *",
  },
];

const processNames = [];
const apps = [];

Array.from([producers, consumers, spiders]).map(t => {
  t.reduce((a, v) => {
    if (!v.hasOwnProperty('name') || v.name.length === 0) {
      console.error('ERROR: process name field is required');
      process.exit(1);
    }
    if (processNames.includes(v.name)) {
      console.error(`ERROR: Duplicate process name declared: ${v.name}. Check required`);
      process.exit(1);
    }

    processNames.push(v.name);
    a.push(
      Object.assign(
        {},
        {
          cwd: PYTHON_CWD,
          combine_logs: true,
          merge_logs: true,
          error_file: path.join(PM2_LOG_DIRECTORY, `${v.name}.log`),
          out_file: path.join(PM2_LOG_DIRECTORY, `${v.name}.log`),
          max_restarts: 10,
          max_memory_restart: MAX_MEMORY_RESTART,
        },
        v,
        (v.hasOwnProperty('cron_restart')) ? {
          cron_restart: v.cron_restart,
          autorestart: false,
        } : null,
      )
    );
    return a
  }, apps)
});

module.exports = {
  apps: apps
};
