# Kubernetes Crypto Price Operator

I was searching for content on Kubernetes [Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) and building [Operators](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) in Python and came across this two-part blog post ([part 1](https://brennerm.github.io/posts/k8s-operators-with-python-part-1.html), [part 2](https://brennerm.github.io/posts/k8s-operators-with-python-part-2.html)). Inspired by that, I decided to build an operator that integrated with the [CoinGecko](https://www.coingecko.com/en) [API](https://www.coingecko.com/en/api) to fetch the current price of a coin in the currency defined in a custom resource.

## How to Use

The steps to install this are pretty straightforward. This assumes you already have a Kubernetes cluster available. If not, the easiest way to test this locally is using [minikube](https://minikube.sigs.k8s.io/docs/).

1. Create the CryptoPrice object using the CRD manifest.

    ```shell
    $ kubectl apply -f crd.yml
    ```

2. Create a ConfigMap with your Slack [webhook](https://api.slack.com/messaging/webhooks) URL.

    ```shell
    $ kubectl create configmap slack-config --from-literal=webhook_url=https://hooks.slack.com/services/XXXXXXXXX/XXXXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXXXX
    ```

3. Deploy the Operator to the cluster.

    ```shell
    $ kubectl apply -f cryptoprices-operator.yml
    ```

4. Create the custom resources.

    ```shell
    $ kubectl apply -f cryptoprice.yml
    ```

As soon as the pod is running the operator should send you a message (example below) with the coin prices in the currencies you defined in the `cryptoprice.yml` file. It will continue to send you a message every hour (3600 seconds) as defined in the `cryptoprices-operator.py` file.

![Slack Message](/slack.png)

If you want to change the interval or only want it to run once, you'll need to modify the `cryptoprices-operator.py` file, build a new container image and push it to a container repository that your cluster has access to. [Here](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) are instructions for using GitHub's container registry.

Once you have pushed your new image, you'll need to update the `image` in the operator definition to point to your new image:

```yaml
...
containers:
- name: cryptoprices-operator
image: ghcr.io/timrcase/cryptoprices-operator:v1.1 <- Change this
imagePullPolicy: IfNotPresent
env:
...
```
