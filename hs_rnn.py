import tensorflow as tf
from tensorflow.contrib import layers
from tensorflow.contrib import rnn  # rnn stuff temporarily in contrib, moving back to code in TF 1.1
import os
import time
import math
import numpy as np
from data_tools import Data_Tools
from data_tools import Progress


class Neural_Network:

	def __init__(self):
		tf.set_random_seed(0)
		self.txt = Data_Tools()
		
		#training vars
		self.seqLength = 30
		self.batchSize = 200
		self.alphabetSize = 98
		self.internalSize = 512
		self.nLayers = 3
		self.learningRate = 0.001  # fixed learning rate
		self.dropout_pkeep = 0.8    # some dropout
		self.trainingDataDir = "training_data/*.txt"
		self.epochs = 10
		
		self.checkpoint = "Checkpoints/rnn_train_1510277210-21000000" #4 hours training hearthstone cards
		self.outputfile = "output.txt"


	def startTraining(self):
		ncnt = 0
	
		# load data, either shakespeare, or the Python source of Tensorflow itself
		codetext, valitext, bookranges = self.txt.read_data_files(self.trainingDataDir, validation=True)

		# display some stats on the data
		epoch_size = len(codetext) // (self.batchSize * self.seqLength)
		self.txt.print_data_stats(len(codetext), len(valitext), epoch_size)

		#
		# the model (see FAQ in README.md)
		#
		lr = tf.placeholder(tf.float32, name='lr')  # learning rate
		pkeep = tf.placeholder(tf.float32, name='pkeep')  # dropout parameter
		batchsize = tf.placeholder(tf.int32, name='batchsize')

		# inputs
		X = tf.placeholder(tf.uint8, [None, None], name='X')    # [ self.batchSize, self.seqLength ]
		Xo = tf.one_hot(X, self.alphabetSize, 1.0, 0.0)                 # [ self.batchSize, self.seqLength, self.alphabetSize ]
		# expected outputs = same sequence shifted by 1 since we are trying to predict the next character
		Y_ = tf.placeholder(tf.uint8, [None, None], name='Y_')  # [ self.batchSize, self.seqLength ]
		Yo_ = tf.one_hot(Y_, self.alphabetSize, 1.0, 0.0)               # [ self.batchSize, self.seqLength, self.alphabetSize ]
		# input state
		Hin = tf.placeholder(tf.float32, [None, self.internalSize*self.nLayers], name='Hin')  # [ self.batchSize, self.internalSize * self.nLayers]

		# using a self.nLayers=3 layers of GRU cells, unrolled self.seqLength=30 times
		# dynamic_rnn infers self.seqLength from the size of the inputs Xo

		# How to properly apply dropout in RNNs: see README.md
		cells = [rnn.GRUCell(self.internalSize) for _ in range(self.nLayers)]
		# "naive dropout" implementation
		dropcells = [rnn.DropoutWrapper(cell,input_keep_prob=pkeep) for cell in cells]
		multicell = rnn.MultiRNNCell(dropcells, state_is_tuple=False)
		multicell = rnn.DropoutWrapper(multicell, output_keep_prob=pkeep)  # dropout for the softmax layer

		Yr, H = tf.nn.dynamic_rnn(multicell, Xo, dtype=tf.float32, initial_state=Hin)
		# Yr: [ self.batchSize, self.seqLength, self.internalSize ]
		# H:  [ self.batchSize, self.internalSize*self.nLayers ] # this is the last state in the sequence

		H = tf.identity(H, name='H')  # just to give it a name

		# Softmax layer implementation:
		# Flatten the first two dimension of the output [ self.batchSize, self.seqLength, self.alphabetSize ] => [ self.batchSize x self.seqLength, self.alphabetSize ]
		# then apply softmax readout layer. This way, the weights and biases are shared across unrolled time steps.
		# From the readout point of view, a value coming from a sequence time step or a minibatch item is the same thing.

		Yflat = tf.reshape(Yr, [-1, self.internalSize])    # [ self.batchSize x self.seqLength, self.internalSize ]
		Ylogits = layers.linear(Yflat, self.alphabetSize)     # [ self.batchSize x self.seqLength, self.alphabetSize ]
		Yflat_ = tf.reshape(Yo_, [-1, self.alphabetSize])     # [ self.batchSize x self.seqLength, self.alphabetSize ]
		loss = tf.nn.softmax_cross_entropy_with_logits(logits=Ylogits, labels=Yflat_)  # [ self.batchSize x self.seqLength ]
		loss = tf.reshape(loss, [batchsize, -1])      # [ self.batchSize, self.seqLength ]
		Yo = tf.nn.softmax(Ylogits, name='Yo')        # [ self.batchSize x self.seqLength, self.alphabetSize ]
		Y = tf.argmax(Yo, 1)                          # [ self.batchSize x self.seqLength ]
		Y = tf.reshape(Y, [batchsize, -1], name="Y")  # [ self.batchSize, self.seqLength ]
		train_step = tf.train.AdamOptimizer(lr).minimize(loss)

		# stats for display
		seqloss = tf.reduce_mean(loss, 1)
		batchloss = tf.reduce_mean(seqloss)
		accuracy = tf.reduce_mean(tf.cast(tf.equal(Y_, tf.cast(Y, tf.uint8)), tf.float32))
		loss_summary = tf.summary.scalar("batch_loss", batchloss)
		acc_summary = tf.summary.scalar("batch_accuracy", accuracy)
		summaries = tf.summary.merge([loss_summary, acc_summary])

		# Init Tensorboard stuff. This will save Tensorboard information into a different
		# folder at each run named 'log/<timestamp>/'. Two sets of data are saved so that
		# you can compare training and validation curves visually in Tensorboard.
		timestamp = str(math.trunc(time.time()))
		summary_writer = tf.summary.FileWriter("log/" + timestamp + "-training")
		validation_writer = tf.summary.FileWriter("log/" + timestamp + "-validation")

		# Init for saving models. They will be saved into a directory named 'checkpoints'.
		# Only the last self.checkpoint is kept.
		if not os.path.exists("Checkpoints"):
			os.mkdir("Checkpoints")
		saver = tf.train.Saver(max_to_keep=1000)
		
		# for display: init the progress bar
		DISPLAY_FREQ = 50
		_50_BATCHES = DISPLAY_FREQ * self.batchSize * self.seqLength
		progress = Progress(DISPLAY_FREQ, size=111+2, msg="Training on next "+str(DISPLAY_FREQ)+" batches")


		# init
		istate = np.zeros([self.batchSize, self.internalSize*self.nLayers])  # initial zero input state
		init = tf.global_variables_initializer()
		sess = tf.Session()
		sess.run(init)
		step = 0
		
		# training loop
		for x, y_, epoch in self.batch_sequencer(codetext, self.batchSize, self.seqLength, self.epochs):

			# train on one minibatch
			feed_dict = {X: x, Y_: y_, Hin: istate, lr: self.learningRate, pkeep: self.dropout_pkeep, batchsize: self.batchSize}
			_, y, ostate = sess.run([train_step, Y, H], feed_dict=feed_dict)

			# log training data for Tensorboard display a mini-batch of sequences (every 50 batches)
			if step % _50_BATCHES == 0:
				feed_dict = {X: x, Y_: y_, Hin: istate, pkeep: 1.0, batchsize: self.batchSize}  # no dropout for validation
				y, l, bl, acc, smm = sess.run([Y, seqloss, batchloss, accuracy, summaries], feed_dict=feed_dict)
				self.txt.print_learning_learned_comparison(x, y, l, bookranges, bl, acc, epoch_size, step, epoch)
				summary_writer.add_summary(smm, step)

			# run a validation step every 50 batches
			# The validation text should be a single sequence but that's too slow (1s per 1024 chars!),
			# so we cut it up and batch the pieces (slightly inaccurate)
			# tested: validating with 5K sequences instead of 1K is only slightly more accurate, but a lot slower.
			if step % _50_BATCHES == 0 and len(valitext) > 0:
				VALI_self.seqLength = 1*1024  # Sequence length for validation. State will be wrong at the start of each sequence.
				bsize = len(valitext) // VALI_self.seqLength
				self.txt.print_validation_header(len(codetext), bookranges)
				vali_x, vali_y, _ = next(self.txt.rnn_minibatch_sequencer(valitext, bsize, VALI_self.seqLength, 1))  # all data in 1 batch
				vali_nullstate = np.zeros([bsize, self.internalSize*self.nLayers])
				feed_dict = {X: vali_x, Y_: vali_y, Hin: vali_nullstate, pkeep: 1.0,  # no dropout for validation
							 batchsize: bsize}
				ls, acc, smm = sess.run([batchloss, accuracy, summaries], feed_dict=feed_dict)
				self.txt.print_validation_stats(ls, acc)
				# save validation data for Tensorboard
				validation_writer.add_summary(smm, step)

			# display a short text generated with the current weights and biases (every 150 batches)
			if step // 3 % _50_BATCHES == 0:
				self.txt.print_text_generation_header()
				ry = np.array([[self.txt.encodeChar(ord("K"))]])
				rh = np.zeros([1, self.internalSize * self.nLayers])
				for k in range(1000):
					ryo, rh = sess.run([Yo, H], feed_dict={X: ry, pkeep: 1.0, Hin: rh, batchsize: 1})
					rc = self.txt.sample_from_probabilities(ryo, topn=10 if epoch <= 1 else 2)
					ry = np.array([[rc]])
					print(chr(self.txt.decodeChar(rc)), end="")
				self.txt.print_text_generation_footer()

			# save a checkpoint (every 500 batches)
			if step // 10 % _50_BATCHES == 0:
				saved_file = saver.save(sess, 'Checkpoints/rnn_train_' + timestamp, global_step=step)
				print("Saved file: " + saved_file)

			# display progress bar
			progress.step(reset=step % _50_BATCHES == 0)

			# loop state around
			istate = ostate
			step += self.batchSize * self.seqLength
		
		
	def StartGenerating(self, numOfChars):
		with tf.Session() as sess:
			new_saver = tf.train.import_meta_graph(self.checkpoint + '.meta')
			new_saver.restore(sess, self.checkpoint)
			x = self.txt.encodeChar(ord("L"))
			x = np.array([[x]])  # shape [self.batchSize, self.seqLength] with self.batchSize=1 and self.seqLength=1
			ncnt = 0
			self.outputfile = "Output_data/output_" +str(math.trunc(time.time()))+".txt"
			file = open(self.outputfile, "w+")
			# initial values
			y = x
			h = np.zeros([1, self.internalSize * self.nLayers], dtype=np.float32)  # [ self.batchSize, self.internalSize * self.nLayers]
			for i in range(numOfChars):
				yo, h = sess.run(['Yo:0', 'H:0'], feed_dict={'X:0': y, 'pkeep:0': 1., 'Hin:0': h, 'batchsize:0': 1})

				# If sampling is be done from the topn most likely characters, the generated text
				# is more credible and more "english". If topn is not set, it defaults to the full
				# distribution (self.alphabetSize)

				# Recommended: topn = 10 for intermediate checkpoints, topn=2 or 3 for fully trained checkpoints

				c = self.txt.sample_from_probabilities(yo, topn=2)
				y = np.array([[c]])  # shape [self.batchSize, self.seqLength] with self.batchSize=1 and self.seqLength=1
				c = chr(self.txt.decodeChar(c))
				print(c, end="")
				file.write(c)
				
				if c == '\n':
					ncnt = 0
				else:
					ncnt += 1
				if ncnt == 100:
					print("")
					ncnt = 0
			file.close
			
	def batch_sequencer(self, raw_data, batch_size, sequence_size, nb_epochs):
		data = np.array(raw_data)
		data_len = data.shape[0]
		# using (data_len-1) because we must provide for the sequence shifted by 1 too
		nb_batches = (data_len - 1) // (batch_size * sequence_size)
		assert nb_batches > 0, "Not enough data, even for a single batch. Try using a smaller batch_size."
		rounded_data_len = nb_batches * batch_size * sequence_size
		xdata = np.reshape(data[0:rounded_data_len], [batch_size, nb_batches * sequence_size])
		ydata = np.reshape(data[1:rounded_data_len + 1], [batch_size, nb_batches * sequence_size])

		for epoch in range(nb_epochs):
			for batch in range(nb_batches):
				x = xdata[:, batch * sequence_size:(batch + 1) * sequence_size]
				y = ydata[:, batch * sequence_size:(batch + 1) * sequence_size]
				x = np.roll(x, -epoch, axis=0)  # to continue the text from epoch to epoch (do not reset rnn state!)
				y = np.roll(y, -epoch, axis=0)
				yield x, y, epoch