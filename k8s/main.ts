import { Construct } from 'constructs';
import { App } from 'cdk8s';
import { Application, PennLabsChart, RedisApplication, CronJob } from '@pennlabs/kittyhawk';

const cronTime = require('cron-time-generator');

export class MyChart extends PennLabsChart {
  constructor(scope: Construct) {
    super(scope);

    const backendImage = 'pennlabs/labs-analytics-backend';
    const secret = "platform"
    const domain = "analytics.pennlabs.org"

    const ingressProps = {
      annotations: {
        ['ingress.kubernetes.io/content-security-policy']: "frame-ancestors 'none';",
        ["ingress.kubernetes.io/protocol"]: "https",
        ["traefik.ingress.kubernetes.io/router.middlewares"]: "default-redirect-http@kubernetescrd"
      }
    }

    new RedisApplication(this, 'redis', {
      deployment: { 
	    image: 'redis/redis-stack-server',
        tag: '6.2.6-v6'
      },
      persistData: true,
    });

    new Application(this, 'backend', {
      deployment: {
        image: backendImage,
        secret,
        replicas: 1,
        env: [],
      },
      ingress: {
        rules: [{
          host: domain,
          paths: ["/analytics"],
          isSubdomain: true,
        }],
        ...ingressProps,
      }
    });
    new CronJob(this, 'load-flush-db', {
      schedule: cronTime.everyDayAt(7),
      image: backendImage,
      secret,
      cmd: ["python", "scripts/flush_db.py", "full"],
      env: []
    });
  }
}

const app = new App();
new MyChart(app);
app.synth();
