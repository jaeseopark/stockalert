# stockalert

```bash
sam build && \
sam deploy \
  --stack-name stockalert \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides NotifySnsArn=BLAH \
  --s3-bucket BLAH \
  --profile BLAH
```
