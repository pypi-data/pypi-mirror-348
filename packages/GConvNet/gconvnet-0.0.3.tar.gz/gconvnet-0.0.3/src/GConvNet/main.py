import torch
import torch.nn as nn

class GConvNet(nn.Module):
    def __init__(self, I, O):
        super(GConvNet, self).__init__()
        self.conv = nn.Conv2d(I, O, (3,1))
    
    def remove(self, C, edge_index):
        T = torch.bincount(edge_index.flatten())
        R = torch.argsort(T)
        R = R[: len(R) // 2]
        for i in range(edge_index.size(0)):
            mask = ~torch.isin(edge_index[i], R)
            edge_index = edge_index[:, mask]
            C = C[:, :, mask]
        return C, edge_index

    def triplets(self, edge_index):
        SRC = edge_index[0]
        TGT = edge_index[1]
        E = SRC.size(0)
        SORTED = torch.argsort(TGT)
        SORTEDTGT = TGT[SORTED]
        LB = torch.searchsorted(SORTEDTGT, SRC)
        UB = torch.searchsorted(SORTEDTGT, SRC, right=True)
        counts = UB - LB
        T = counts.sum()
        if T == 0:
            return torch.empty((3, 0), dtype=edge_index.dtype, device=edge_index.device)
        R = torch.arange(E, device=edge_index.device).repeat_interleave(counts)
        CUM = torch.cumsum(counts, dim=0)
        G = CUM - counts
        O = torch.arange(T, device=edge_index.device) - G[R]
        ALL = SORTED[LB[R] + O]
        A = SRC[ALL]
        B = TGT[ALL]
        C = TGT[R]
        return torch.stack([A, B, C], dim=0)
    
    def sum(self, C, edge_index):
        unique, inverse = torch.unique(edge_index[0], sorted=True, return_inverse=True)
        S = torch.zeros(C.size(0), C.size(1), unique.size(0), device=C.device)
        S = S.scatter_add(2, inverse.unsqueeze(0).unsqueeze(0).expand_as(C), C)
        counts = torch.bincount(inverse).to(C.device)
        return S / counts.view(1, 1, -1)
    
    def forward(self, x, edge_index):
        if len(x.shape) > 1:
            edge_index = edge_index[:, edge_index[0].argsort()]
            if edge_index.size(0) < 3:
                edge_index = self.triplets(edge_index)
                edge_index = edge_index[:, edge_index[0].argsort()]
            
            INPUT = torch.stack([x[edge_index[0]], x[edge_index[1]], x[edge_index[2]]], dim=1)
            INPUT = INPUT.permute(2, 1, 0)
            C = self.conv(INPUT)
            if x.size(0) > 3:
                C, edge_index = self.remove(C, edge_index)
                x = self.sum(C, edge_index).squeeze(1).permute(1, 0)
                _, new_indices = torch.unique(edge_index, return_inverse=True)
                edge_index = new_indices.view(edge_index.shape)
            else:
                x = x.mean(dim=0)
        return x, edge_index