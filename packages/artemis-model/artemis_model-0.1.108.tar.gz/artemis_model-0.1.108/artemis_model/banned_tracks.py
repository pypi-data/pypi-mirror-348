"""Banned Tracks per Zone Model"""

from sqlalchemy import UUID, Column, Integer

from artemis_model.base import AuditMixin, TimeStampMixin, CustomSyncBase, CustomBase


class BannedTracksMixin(TimeStampMixin, AuditMixin):
    """Banned Tracks per Zone Model"""
    __allow_unmapped__ = True
    
    zone_id: int = Column(Integer, primary_key=True)
    track_id: UUID = Column(UUID(as_uuid=True), primary_key=True)


class BannedTracksSync(CustomSyncBase, BannedTracksMixin):
    """Banned Tracks per Zone Model"""
    pass


class BannedTracks(CustomBase, BannedTracksMixin):
    """Banned Tracks per Zone Model"""
    pass
