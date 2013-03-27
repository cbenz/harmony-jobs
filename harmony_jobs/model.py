# -*- coding: utf-8 -*-


import datetime

from biryani1.strings import slugify
from biryani1.baseconv import check
from biryani1.objectconv import object_to_clean_dict
from suq.monpyjama import Mapper, Wrapper


class Projects(Mapper, Wrapper):
    collection_name = 'projects'

    filename = None
    slug = None
    status = False
    step = 0
    upload_at = None

    def save(self, *args, **kwargs):
        if self.upload_at is None:
            self.upload_at = datetime.datetime.utcnow()

        # find a unique slug based on filename
        if self.slug is None:
            slug = slugify(self.filename)
            distinguish = 1
            while True:
                proposal = slug if distinguish == 1 else '%s-%d' % (slug, distinguish)
                if not Projects.find_one({'slug': proposal}):
                    slug = proposal
                    break
                distinguish += 1
            self.slug = slug

        return super(Projects, self).save(*args, **kwargs)

    def to_bson(self):
        return check(object_to_clean_dict(self))
