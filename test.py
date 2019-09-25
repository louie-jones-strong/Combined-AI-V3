def TensorflowTest():
    try:
        print("testing tensorflow")

        import tensorflow as tf

        # Simple hello world using TensorFlow

        # Create a Constant op
        # The op is added as a node to the default graph.
        #
        # The value returned by the constructor represents the output
        # of the Constant op.
        hello = tf.constant('Hello, TensorFlow!')

        # Start tf session
        sess = tf.Session()

        # Run the op
        print(sess.run(hello))
    except Exception as error:
        self.Logger.LogError(error)
    return


def TfLearnTest():
    try:
        print("testing TfLearn")

        import tflearn

    except Exception as error:
        self.Logger.LogError(error)
    return
