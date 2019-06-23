import matplotlib.pyplot as plt
import networkx as nx

class TreeVisualiser:

	def __init__(self, dataSetManager):
		self.DataSetManager = dataSetManager
		self.DataSetManager.LoadTableInfo()
		startBoard = "[0, 0, 0, 0, 0, 0, 0, 0, 0]"
		self.Tree = nx.Graph()
		self.Tree.add_node(startBoard)
		self.Pos = {}
		self.DepthNumNodes = {}
		self.Labels = {}

		depth = 9
		self.Pos[startBoard] = [0,depth*100]
		self.Labels[startBoard] = startBoard
		self.DepthNumNodes[depth] = 1

		self.BuildTree(startBoard, depth-1)
		self.ShowTree()
		return
	
	def BuildTree(self, key, depth):
		found, boardInfo = self.DataSetManager.GetBoardInfo(key)
		if found:
			for movekey, moveValue in boardInfo.Moves.items():

				for outComesKey, outComesValue in moveValue.MoveOutComes.items():

					self.Tree.add_edge(key, outComesKey)

					
					if outComesKey not in self.Pos:
						if depth not in self.DepthNumNodes:
							self.DepthNumNodes[depth] = 0

						self.Pos[outComesKey] = [self.DepthNumNodes[depth], depth*100]
						self.DepthNumNodes[depth] += 1
						self.Labels[outComesKey] = outComesKey

					if depth > 1:
						self.BuildTree(outComesKey, depth-1)
		return

	def ShowTree(self):

		plt.subplot(111)
		#nx.draw_shell(self.Tree, with_labels=True, font_weight='bold')

		nx.draw_networkx_nodes(self.Tree, self.Pos, self.Labels)

		# edges
		nx.draw_networkx_edges(self.Tree, self.Pos, alpha=0.5)

		print("Nodes: "+str(self.Tree.number_of_nodes()))
		print("edges: "+str(self.Tree.number_of_edges()))
		#plt.axis('off')
		#plt.savefig("tree.png", transparent=False)
		plt.show()
		return