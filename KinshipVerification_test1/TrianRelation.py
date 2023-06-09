import tensorflow as tf
import numpy as np
import random
import os
import datetime
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
import matplotlib.pyplot as plt

# how to improve: add more layers/use more data to train/change the number of the fold, may change the result of validation accuracy
# change accuracy function

from random import sample

# readme we can use two ways to test the project
# 1 similarity
# 2 NN this is a low feature algorithm + kfold


lable_set = ['f-d', 'f-s', 'm-d', 'm-s']

# general Variables
batchsize = 100  # batch size must be even
best_iterations = 10000
hiddenunit = 80
ita = 0.7
keep_pro = 0.75

# loadFeature vector
def loadInFeatureVect(dir):
    # combine two vector into one
    vectors = []
    labels = []
    # we fisrt train in order :father-daughter, father son, mother daughter, mother-son
    # loadfeature vectors acquire all the features
    # acquire file list


    for s in os.listdir(dir):
        newdir = os.path.join(dir, s)
        vectors1 = np.load(newdir)
        vectors.extend(vectors1)
        if s.find("f-d") >= 0:
            labels1 = np.zeros(len(vectors1))
            labels.extend(labels1)
        elif s.find("f-s") >= 0:  # positive data
            labels2 = np.zeros(len(vectors1))
            labels.extend(labels2)
        elif s.find("m-d") >= 0:  # positive data
            labels2 = np.zeros(len(vectors1))
            labels.extend(labels2)
        elif s.find("m-s") >= 0:  # positive data
            labels2 = np.zeros(len(vectors1))
            labels.extend(labels2)
        else:  # negative data
            labels2 = -1 * np.ones(len(vectors1))
            labels.extend(labels2)

    return np.array(vectors), np.array(labels)


def loadInFeatureVect_test(dir):
    # combine two vector into one
    vectors = []
    labels = []
    # we fisrt train in order :father-daughter, father son, mother daughter, mother-son
    # loadfeature vectors acquire all the features
    # acquire file list
    # dir='../128vectors-k2/'

    for s in os.listdir(dir):
        newdir = os.path.join(dir, s)
        vectors1 = np.load(newdir)
        vectors.extend(vectors1)
        if s.find("f-d") >= 0:
            labels1 = np.zeros(len(vectors1))
            labels.extend(labels1)
        elif s.find("f-s") >= 0:  # positive data
            labels2 = np.zeros(len(vectors1))
            labels.extend(labels2)
        elif s.find("m-d") >= 0:  # positive data
            labels2 = np.zeros(len(vectors1))
            labels.extend(labels2)
        elif s.find("m-s") >= 0:  # positive data
            labels2 = np.zeros(len(vectors1))
            labels.extend(labels2)
        else:  # negative data
            labels2 = -1 * np.ones(len(vectors1))
            labels.extend(labels2)

    return np.array(vectors), np.array(labels)


def feature_inputdata_skearn(vectors, labels):
    # combine parent and child feature into one vector
    comVec = []
    comLab = []
    length = vectors.shape[0]
    for i in range(0, length, 2):
        v = []
        v.extend(vectors[i])
        v.extend(vectors[i + 1])

        comVec.append(v)
        if labels[i] == 0:
            comLab.append(1)
        else:
            comLab.append(0)


    indices = np.arange(len(comVec))
    np.random.shuffle(indices)

    comVec1 = []
    comLab1 = []
    for i in indices:
        comVec1.append(comVec[i])
        comLab1.append(comLab[i])

    # print(comLab1)
    return np.array(comVec1), np.array(comLab1)

def feature_inputdata(vectors, labels):
    # combine parent and child feature into one vector
    comVec = []
    comLab = []
    length = vectors.shape[0]
    for i in range(0, length, 2):
        v = []
        v.extend(vectors[i])
        v.extend(vectors[i + 1])

        comVec.append(v)
        if labels[i] == 0:
            comLab.append([1, 0])
        else:
            comLab.append([0, 1])


    indices = np.arange(len(comVec))
    np.random.shuffle(indices)

    comVec1 = []
    comLab1 = []
    for i in indices:
        comVec1.append(comVec[i])
        comLab1.append(comLab[i])

    # print(comLab1)
    return np.array(comVec1), np.array(comLab1)


# to be changed
def getimageFeaturebynxtbatch(vectors, labels, batchsize):
    # acquire corrsponding batch vectors
    batch_ys = []
    batch_xs = []
    # batch_xs = np.zeros([batchsize,vectors.shape(0)])
    #  for i in range(batchsize):
    #      num = randint(1, len(vectors) - 1)
    #      batch_ys.append(labels[num])
    #      batch_xs.applend(vectors[num])

    indxs = random.sample(range(0, len(vectors)), batchsize)
    for i in range(len(indxs)):
        batch_ys.append(labels[indxs[i]])
        batch_xs.append(vectors[indxs[i]])

    return np.array(batch_xs), np.array(batch_ys)




# ts_vectors,ts_labels =loadInFeatureVect()
# test input------- done
# tr_vectors = np.load('../128vectors/f-d.npy')


def kv_similarity():
    # use similarity between two features
    accuracy = 0
    loss = 0

    return accuracy, loss


# def getdataByindex(indices_tr,indices_tst, vectx,vecty):
#     tr_vectx_result =[]
#     tr_vecty_result = []
#     tst_vectx_result = []
#     tst_vecty_result = []
#     for i in indices_tr:
#         tr_vectx_result.append(vectx[i])
#         tr_vecty_result.append(vecty[i])
#     for i in indices_tst:
#         tst_vectx_result.append(vectx[i])
#         tst_vecty_result.append(vecty[i])
#
#     return tr_vectx_result,tr_vecty_result,tst_vectx_result,tst_vecty_result

def Train_Relation_NN():
    x = tf.placeholder(tf.float32, [None, 256])  # we input 2 vector as our input 128*2
    y_ = tf.placeholder(tf.float32, [None, 2])  # we have four kinds of relationship
    #
    # w1 = tf.Variable(tf.zeros([256, hiddenunit]))  # how many items in each x,unit of hidden layer]
    w1 = tf.Variable(tf.truncated_normal([256, hiddenunit], stddev=0.1))
    b1 = tf.Variable(tf.zeros([hiddenunit]))  # how many hidden unit in each layer
    w2 = tf.Variable(tf.truncated_normal([hiddenunit, hiddenunit], stddev=0.1))
    b2 = tf.Variable(tf.zeros([hiddenunit]))  # how many hidden unit in each layer
    w3 = tf.Variable(tf.zeros([hiddenunit, 2]))  # [how many items in each x,unit of hidden layer],初始值是0
    b3 = tf.Variable(tf.zeros([2]))
    keep_prob = tf.placeholder(tf.float32)

    # layer 1
    # relu
    # logistic
    # softmax
    nnhlyer1 = tf.nn.relu(tf.matmul(x, w1) + b1)
    h_fc1_drop1 = tf.nn.dropout(nnhlyer1, keep_prob)  # avoid overfit
    # layer 2
    nnhlyer2 = tf.nn.sigmoid(tf.matmul(h_fc1_drop1, w2) + b2)
    h_fc1_drop2 = tf.nn.dropout(nnhlyer2, keep_prob)  # avoid overfit
    # layer 3
    y_nn = tf.nn.softmax(tf.matmul(h_fc1_drop2, w3) + b3)
    # loss
    cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y_nn),
                                                  reduction_indices=[1]))  # loss

    # cross_entropy = -tf.reduce_sum(y_*tf.log(y_nn))

    correctPred = tf.equal(tf.argmax(y_nn, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correctPred, tf.float32))

    # change
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=(tf.matmul(h_fc1_drop2, w3) + b3), labels=y_))

    # update
    train_step = tf.train.GradientDescentOptimizer(ita).minimize(cross_entropy)

    # init
    init = tf.global_variables_initializer()

    # 10 -fold
    # train iterations
    # save accuracy
    # trans list into array for cross validation
    # array_trvect=np.array(tr_vectors)
    # array_trlab = np.array(tr_labels)
    #
    # tst_accuracy_setallfolds =[]
    # tr_accuracy_setallfolds =[]
    # iterations_set = [40000]#np.arange(6000,18000,4000)
    # #np.random.shuffle(tr_vectors)
    # kf = KFold(n_splits=10)#, shuffle=True, # try 20 fold
    #
    # #k-fold cross validation
    # for j in iterations_set:
    #     print("ieration:%d"%j)
    #     #KFold(n_splits=10, random_state=None, shuffle=False)
    #     accuracy_set_tr = []
    #     accuracy_set_tst = []
    #     # Session
    #     # init
    #     init = tf.global_variables_initializer()
    #     sess = tf.InteractiveSession()
    #     sess.run(init)
    #
    #     for train_index, test_index in kf.split(tr_vectors):
    #         X_train, X_test = tr_vectors[train_index], tr_vectors[test_index]
    #         y_train, y_test = tr_labels[train_index], tr_labels[test_index]
    #         for i in range(j):
    #             #random
    #             batch_xs, batch_ys = getimageFeaturebynxtbatch(X_train,y_train,batchsize)
    #             sess.run([cross_entropy,train_step], feed_dict={x: batch_xs, y_: batch_ys,keep_prob:keep_pro})
    #             # if i % 20 == 0:
    #             #     # correct_prediction = tf.equal(tf.argmax(y_nn, 1), tf.argmax(y_, 1))
    #             #     # accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    #             #     # print ("Setp: ", i, "Accuracy: ",sess.run(accuracy, feed_dict={x: batch_xs, y_: batch_ys}))
    #             #     save_path = saver.save(sess, "models/pretrained_lstm.ckpt", global_step=i)
    #             #     print("saved to %s" % save_path)
    #             #     summary = sess.run(merged, {x: batch_xs, y_: batch_ys,keep_prob: 1.0})
    #             #     writer.add_summary(summary, i)
    #         correct_prediction = tf.equal(tf.argmax(y_nn, 1), tf.argmax(y_, 1))
    #         accuracy_validate = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    #         accuracy_fold_tst= sess.run(accuracy_validate, feed_dict={x: X_test, y_: y_test,keep_prob: 1.0})
    #         accuracy_fold_tr = sess.run(accuracy_validate, feed_dict={x: X_train, y_: y_train,keep_prob: 1.0})
    #         print("train accuracy:%f,test accuracy :%f"%(accuracy_fold_tr,accuracy_fold_tst))
    #         accuracy_set_tr.append(accuracy_fold_tr)
    #         accuracy_set_tst.append(accuracy_fold_tst)
    #
    #     tst_accuracy_setallfolds.append(np.mean(accuracy_set_tst))
    #     tr_accuracy_setallfolds.append(np.mean(accuracy_set_tr))
    #
    #         # save accuracy of each fold
    #     #acquire best mean accuracy select best iteration
    # best_iterations=iterations_set[tst_accuracy_setallfolds.index(max(tst_accuracy_setallfolds))]
    # print("best iterations:%d and max test accuracy:%f "%(best_iterations,max(tst_accuracy_setallfolds)))
    #
    #
    #
    #
    # #plot
    # plt.plot(iterations_set, tr_accuracy_setallfolds, '-', label=u'train accuracy')
    # plt.plot(iterations_set, tst_accuracy_setallfolds, '-', label=u'validate accuracy')
    # plt.xlabel('# of iterations')
    # plt.ylabel('prediction accuracy')
    # plt.legend()
    # plt.show()

    # run best iteration
    # best_iterations =20000
    # Session
    # best_iterations=150000
    sess = tf.InteractiveSession()
    sess.run(init)
    saver = tf.train.Saver()
    #saver.restore(sess, tf.train.latest_checkpoint('models')) for test
    tf.summary.scalar('Loss', cross_entropy)
    tf.summary.scalar('Accuracy', accuracy)
    merged = tf.summary.merge_all()
    logdir = "tensorboard/" + "rela"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + "/"
    writer = tf.summary.FileWriter(logdir, sess.graph)

    for i in range(best_iterations):
        # random
        batch_xs, batch_ys = getimageFeaturebynxtbatch(tr_vectors, tr_labels, batchsize)
        sess.run([cross_entropy, train_step], feed_dict={x: batch_xs, y_: batch_ys, keep_prob: keep_pro})
        if i % 20 == 0:
            save_path = saver.save(sess, "models_rela/pretrained_relation.ckpt", global_step=i)
            print("saved to %s" % save_path)
            summary = sess.run(merged, {x: batch_xs, y_: batch_ys, keep_prob: 1.0})
            writer.add_summary(summary, i)
    correct_prediction = tf.equal(tf.argmax(y_nn, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    accuracy_tr = sess.run(accuracy, feed_dict={x: tr_vectors, y_: tr_labels, keep_prob: 1.0})
    accuracy_tst = sess.run(accuracy, feed_dict={x: tst_vectors, y_: tst_labels, keep_prob: 1.0})


    print("whole train data accuracy:%f" % accuracy_tr)
    print("whole test data accuracy:%f" % accuracy_tst)


    writer.close()

def Train_Relation_logistic():
    x = tf.placeholder(tf.float32, [None, 256])  # we input 2 vector as our input 128*2
    y_ = tf.placeholder(tf.float32, [None, 2])  # we have four kinds of relationship
    #
    # w1 = tf.Variable(tf.zeros([256, hiddenunit]))  # how many items in each x,unit of hidden layer]
    w1 = tf.Variable(tf.truncated_normal([256, 2], stddev=0.1))
    b1 = tf.Variable(tf.zeros([2]))  # how many hidden unit in each layer



    y_nn = tf.nn.softmax(tf.matmul(x, w1) + b1)
    # loss
    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=(y_nn), labels=y_))

    # cross_entropy = -tf.reduce_sum(y_*tf.log(y_nn))

    correctPred = tf.equal(tf.argmax(y_nn, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correctPred, tf.float32))

    # change

    # update
    train_step = tf.train.GradientDescentOptimizer(ita).minimize(cross_entropy)

    # init
    init = tf.global_variables_initializer()

    # 10 -fold
    # train iterations
    # save accuracy
    # trans list into array for cross validation
    # array_trvect=np.array(tr_vectors)
    # array_trlab = np.array(tr_labels)
    #
    # tst_accuracy_setallfolds =[]
    # tr_accuracy_setallfolds =[]
    # iterations_set = [40000]#np.arange(6000,18000,4000)
    # #np.random.shuffle(tr_vectors)
    # kf = KFold(n_splits=10)#, shuffle=True, # try 20 fold
    #
    # #k-fold cross validation
    # for j in iterations_set:
    #     print("ieration:%d"%j)
    #     #KFold(n_splits=10, random_state=None, shuffle=False)
    #     accuracy_set_tr = []
    #     accuracy_set_tst = []
    #     # Session
    #     # init
    #     init = tf.global_variables_initializer()
    #     sess = tf.InteractiveSession()
    #     sess.run(init)
    #
    #     for train_index, test_index in kf.split(tr_vectors):
    #         X_train, X_test = tr_vectors[train_index], tr_vectors[test_index]
    #         y_train, y_test = tr_labels[train_index], tr_labels[test_index]
    #         for i in range(j):
    #             #random
    #             batch_xs, batch_ys = getimageFeaturebynxtbatch(X_train,y_train,batchsize)
    #             sess.run([cross_entropy,train_step], feed_dict={x: batch_xs, y_: batch_ys,keep_prob:keep_pro})
    #             # if i % 20 == 0:
    #             #     # correct_prediction = tf.equal(tf.argmax(y_nn, 1), tf.argmax(y_, 1))
    #             #     # accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    #             #     # print ("Setp: ", i, "Accuracy: ",sess.run(accuracy, feed_dict={x: batch_xs, y_: batch_ys}))
    #             #     save_path = saver.save(sess, "models/pretrained_lstm.ckpt", global_step=i)
    #             #     print("saved to %s" % save_path)
    #             #     summary = sess.run(merged, {x: batch_xs, y_: batch_ys,keep_prob: 1.0})
    #             #     writer.add_summary(summary, i)
    #         correct_prediction = tf.equal(tf.argmax(y_nn, 1), tf.argmax(y_, 1))
    #         accuracy_validate = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    #         accuracy_fold_tst= sess.run(accuracy_validate, feed_dict={x: X_test, y_: y_test,keep_prob: 1.0})
    #         accuracy_fold_tr = sess.run(accuracy_validate, feed_dict={x: X_train, y_: y_train,keep_prob: 1.0})
    #         print("train accuracy:%f,test accuracy :%f"%(accuracy_fold_tr,accuracy_fold_tst))
    #         accuracy_set_tr.append(accuracy_fold_tr)
    #         accuracy_set_tst.append(accuracy_fold_tst)
    #
    #     tst_accuracy_setallfolds.append(np.mean(accuracy_set_tst))
    #     tr_accuracy_setallfolds.append(np.mean(accuracy_set_tr))
    #
    #         # save accuracy of each fold
    #     #acquire best mean accuracy select best iteration
    # best_iterations=iterations_set[tst_accuracy_setallfolds.index(max(tst_accuracy_setallfolds))]
    # print("best iterations:%d and max test accuracy:%f "%(best_iterations,max(tst_accuracy_setallfolds)))
    #
    #
    #
    #
    # #plot
    # plt.plot(iterations_set, tr_accuracy_setallfolds, '-', label=u'train accuracy')
    # plt.plot(iterations_set, tst_accuracy_setallfolds, '-', label=u'validate accuracy')
    # plt.xlabel('# of iterations')
    # plt.ylabel('prediction accuracy')
    # plt.legend()
    # plt.show()

    # run best iteration
    # best_iterations =20000
    # Session
    # best_iterations=150000
    sess = tf.InteractiveSession()
    sess.run(init)
    saver = tf.train.Saver()
    #saver.restore(sess, tf.train.latest_checkpoint('models')) for test
    tf.summary.scalar('Loss', cross_entropy)
    tf.summary.scalar('Accuracy', accuracy)
    merged = tf.summary.merge_all()
    logdir = "tensorboard/" + "rela"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + "/"
    writer = tf.summary.FileWriter(logdir, sess.graph)

    for i in range(best_iterations):
        # random
        batch_xs, batch_ys = getimageFeaturebynxtbatch(tr_vectors, tr_labels, batchsize)
        sess.run([cross_entropy, train_step], feed_dict={x: batch_xs, y_: batch_ys})
        if i % 20 == 0:
            save_path = saver.save(sess, "models_rela/pretrained_relation.ckpt", global_step=i)
            print("saved to %s" % save_path)
            summary = sess.run(merged, {x: batch_xs, y_: batch_ys})
            writer.add_summary(summary, i)
    correct_prediction = tf.equal(tf.argmax(y_nn, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    accuracy_tr = sess.run(accuracy, feed_dict={x: tr_vectors, y_: tr_labels})
    accuracy_tst,y_nn = sess.run([accuracy,y_nn], feed_dict={x: tst_vectors, y_: tst_labels})
    np.save('y_nn_logistic', y_nn)

    print("whole train data accuracy:%f" % accuracy_tr)
    print("whole test data accuracy:%f" % accuracy_tst)


    writer.close()
def sklearnlogistic():
    # We use SAGA solver


    clf = LogisticRegression(penalty='l1',max_iter=20)
    clf.fit(tr_vectors, tr_labels)
    y_pred = clf.predict(tst_vectors)
    accuracy = np.sum(y_pred == tst_labels) / tst_labels.shape[0]
    print(accuracy)


# print sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels})

# test
# input data
# each vector size is 128


# train data  smilefiw
dir = '../128vectors-new1/'
tr_vectors, tr_labels = loadInFeatureVect(dir)
tr_vectors, tr_labels = feature_inputdata(tr_vectors, tr_labels)
print(tr_vectors.shape[0])
# test data  kinface
dir1 = '../128vectors/'
tst_vectors, tst_labels = loadInFeatureVect_test(dir1)
tst_vectors, tst_labels = feature_inputdata(tst_vectors, tst_labels)

# dir1 = '../128vectors-kinface_f-d/'
# tst_vectorsfd, tst_labelsfd = loadInFeatureVect_test(dir1)
# tst_vectorsfd, tst_labelsfd = feature_inputdata(tst_vectorsfd, tst_labelsfd)
# dir1 = '../128vectors-kinface_f-s/'
# tst_vectorsfs, tst_labelsfs = loadInFeatureVect_test(dir1)
# tst_vectorsfs, tst_labelsfs = feature_inputdata(tst_vectorsfs, tst_labelsfs)
# dir1 = '../128vectors-kinface_m-d/'
# tst_vectorsmd, tst_labelsmd = loadInFeatureVect_test(dir1)
# tst_vectorsmd, tst_labelsmd = feature_inputdata(tst_vectorsmd, tst_labelsmd)
# dir1 = '../128vectors-kinface_m-s/'
# tst_vectorsms, tst_labelsms = loadInFeatureVect_test(dir1)
# tst_vectorsms, tst_labelsms = feature_inputdata(tst_vectorsms, tst_labelsms)

Train_Relation_logistic()


#sklearn================

# dir = '../128vectors-new1/'
# tr_vectors, tr_labels = loadInFeatureVect(dir)
# tr_vectors, tr_labels = feature_inputdata_skearn(tr_vectors, tr_labels)
# print(tr_vectors.shape[0])
# # test data  kinface
# dir1 = '../128vectors/'
# tst_vectors, tst_labels = loadInFeatureVect_test(dir1)
# tst_vectors, tst_labels = feature_inputdata_skearn(tst_vectors, tst_labels)
# sklearnlogistic()





# print('len of verctor2 = %d'%len(tr_vectors))



