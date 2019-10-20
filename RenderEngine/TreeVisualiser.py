import matplotlib.pyplot as plt
import networkx as nx
import time

class TreeVisualiser:

	def __init__(self, dataSetManager):
		self.DataSetManager = dataSetManager
		self.MaxDepthFound = 0

		self.ClearTree()
		self.MaxDepth = 100
		self.EdgeCapPerNode = 0

		self.LastOutput = time.time()
		while True:
			self.DataSetManager.LoadTableInfo()

			self.LastLoadTime = time.time()
			self.LastOutput = time.time()
			self.ClearTree()

			for boardKey, _ in self.DataSetManager.StartingBoards.items():
				found, boardInfo = self.DataSetManager.GetBoardInfo(boardKey)
				if found:
					self.BuildTree(boardKey)

			self.ShowTree()

			delta = time.time()-self.LastLoadTime
			if delta < 60:
				print("Sleeping For: "+str(60-delta))
				time.sleep(60-delta)
		return

	def ClearTree(self):
		self.Tree = nx.Graph()
		self.Pos = {}
		self.DepthNumNodes = {}
		self.Labels = {}
		self.FinishedNodes = []
		self.NonFinishedNodes = []
		self.MaxDepthFound = 0
		return
	
	def BuildTree(self, key, depth=0):
		if key in self.Labels:
			return

		if depth not in self.DepthNumNodes:
			self.DepthNumNodes[depth] = 0
			if depth > self.MaxDepthFound:
				self.MaxDepthFound = depth

		x = self.DepthNumNodes[depth]
		if x % 2 == 0:
			x *= -1
			x += 1

		x /= 2
		y = -depth*100

		self.Pos[key] = [x,y]
		self.DepthNumNodes[depth] += 1
		self.Labels[key] = key

		found, boardInfo = self.DataSetManager.GetBoardInfo(key)
		if found:
			if boardInfo.Finished:
				self.FinishedNodes += [key]
			else:
				self.NonFinishedNodes += [key]

			if time.time() - self.LastOutput >= 5:
				self.ShowTree()
				self.LastOutput = time.time()

			if depth <= self.MaxDepth:
				edges = 0
				for movekey, moveValue in boardInfo.Moves.items():
					for outComesKey, outComesValue in moveValue.MoveOutComes.items():
						if edges < self.EdgeCapPerNode:
							self.Tree.add_edge(key, outComesKey)
							edges += 1
						self.BuildTree(outComesKey, depth+1)
		else:
			self.FinishedNodes += [key]
		return

	def ShowTree(self):

		#plt.subplot()
		plt.plot()

		nx.draw_networkx_nodes(self.Tree, self.Pos, nodelist=self.NonFinishedNodes, node_color='r', node_size=100)
		nx.draw_networkx_nodes(self.Tree, self.Pos, nodelist=self.FinishedNodes, node_color='g', node_size=100)
		# edges
		nx.draw_networkx_edges(self.Tree, self.Pos, alpha=0.5)

		#nx.draw_networkx_labels(self.Tree, self.Pos, self.Labels)

		for layerIndex in range(self.MaxDepthFound+1):
			x = 0
			y = -layerIndex*100
			plt.text(x, y, "move:"+str(layerIndex+1), fontsize=10, horizontalalignment='center', verticalalignment='center')

		print("Nodes: "+str(self.Tree.number_of_nodes()))
		print("edges: "+str(self.Tree.number_of_edges()))
		plt.axis('off')
		#plt.savefig("tree.svg", transparent=False)
		plt.show()
		return
