# Storage (cards)

Storage's first part, in the data program
([RFC 0011](https://github.com/pnut-labs/design/blob/master/rfcs/0011-storage.md)): the card in each slot the board's
description gives, mounted at `/media/sd<n>` as the program starts, FAT
only, never formatted; the `storage` topic says what is mounted. Storage
writes nothing on a card.

Interface: [Storage](../interfaces/storage.md).
