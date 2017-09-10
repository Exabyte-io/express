# exabyte-express
ExPreSS: Exabyte Property Ex(ss)tractor, Sourcer, Serializer class.


## Run tests
Follow the below steps to run ExPrESS tests:

1. Download `express-tests-data.tgz` and extract it:

```bash
cd tests
wget http://files.exabyte.io:18/apps/express-tests-data.tgz
tar zxvf express-tests-data.tgz
``` 

2. Setup Python environment according to the attached screenshot:

![python-environment](https://user-images.githubusercontent.com/10528238/29536164-956525fe-8671-11e7-91ec-f0e9c71621ad.png)

3. Configure PyCharm according to the attached screenshots to run unit and integration tests:

![unit-tests](https://user-images.githubusercontent.com/10528238/29536187-adfb0656-8671-11e7-8ba0-b6e7e7fca42c.png)

![integration-tests](https://user-images.githubusercontent.com/10528238/29536163-955f839c-8671-11e7-90e0-b4003e4b4273.png)


## Re-generate input data
In order to re-generate input data for tests you should go to each test directory located and run `sh run.sh` command. 
Please note that the command needs to be executed on master node where module files and applications are installed. 
After re-running the tests you should create a new `express-tests-data.tgz` file and push to file server:

```bash
cd tests
tar zcvf express-tests-data.tgz data
scp express-tests-data.tgz root@exabyte.io:/www/files/apps/express-tests-data.tgz
```
