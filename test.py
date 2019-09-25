def TensorflowTest():
    try:
        print("testing tensorflow")

        import tensorflow

        # Simple hello world using TensorFlow

        # Create a Constant op
        # The op is added as a node to the default graph.
        #
        # The value returned by the constructor represents the output
        # of the Constant op.
        hello = tensorflow.constant('Hello, TensorFlow!')

        # Start tf session
        sess = tensorflow.Session()

        # Run the op
        print(sess.run(hello))
    except Exception as error:
        print(error)
    return


def TfLearnTest():
    try:
        print("testing TfLearn")

        import tflearn

    except Exception as error:
        print(error)
    return
